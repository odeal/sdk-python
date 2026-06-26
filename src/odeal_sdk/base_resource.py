"""
Odeal SDK Base Resource Modülü.

Bu modül, tüm API resource sınıflarının türediği temel sınıfı içerir.
HTTP isteklerini yönetir, validation yapar ve ortak işlevsellik sağlar.
"""

import asyncio
import json
import re
import urllib.request
import urllib.error
import urllib.parse
import time
from typing import Any, Dict, List, Optional, Union

from .odeal_config import OdealConfig
from .multipart_body import MultipartBody
from .exceptions import (
    OdealApiException, OdealValidationException,
    OdealAuthenticationException, OdealForbiddenException,
    OdealNotFoundException, OdealRateLimitException,
)
from .utils import object_to_dict
from .sanitizer import sanitize_json

from .interceptor import RequestContext, ResponseContext
from .circuit_breaker import OdealCircuitBreaker, OdealCircuitOpenException


class BaseResource:
    """
    Tüm API resource sınıflarının türediği temel sınıf.
    
    HTTP isteklerinin gönderilmesi, yanıtların işlenmesi, validation
    ve hata yönetimi gibi temel işlevleri içerir.
    
    Attributes:
        config: SDK yapılandırma ayarları.
    """
    
    AGENT = "OdealSdkPythonClient/0.1.5"
    
    def __init__(self, config: OdealConfig):
        """
        BaseResource sınıfının yeni bir örneğini oluşturur.
        
        Args:
            config: SDK yapılandırma ayarları.
        """
        self.config = config
        self._circuit_breaker = None
        if getattr(self.config, 'circuit_breaker_enabled', False):
            self._circuit_breaker = OdealCircuitBreaker(
                failure_threshold=getattr(self.config, 'circuit_breaker_threshold', 5),
                reset_timeout_ms=getattr(self.config, 'circuit_breaker_reset_ms', 60000)
            )

    def _fill_config_defaults(self, obj: Any) -> None:
        """
        Model içindeki _config_map haritasını kullanarak, boş (None) alanları
        Config dosyasındaki değerlerle doldurur. Rekürsif çalışır.
        
        Args:
            obj: Config değerleri ile doldurulacak model objesi.
        """
        if obj is None:
            return

        # Liste ise elemanları dön
        if isinstance(obj, list):
            for item in obj:
                self._fill_config_defaults(item)
            return

        # Obje üzerinde _config_map varsa işlemi yap
        if hasattr(obj, "_config_map") and isinstance(obj._config_map, dict):
            for field_name, config_attr in obj._config_map.items():
                # Eğer modeldeki alan boşsa (None)
                if getattr(obj, field_name, None) is None:
                    # Config'den değeri al
                    config_val = getattr(self.config, config_attr, None)
                    # Config'de değer varsa modele ata
                    if config_val is not None:
                        setattr(obj, field_name, config_val)
        
        # İç içe objeleri (Nested Models) kontrol et
        if hasattr(obj, "__dict__"):
            for val in obj.__dict__.values():
                # Primitive olmayan (Model veya List) yapıları tekrar kontrol et
                if hasattr(val, "_config_map") or isinstance(val, list):
                    self._fill_config_defaults(val)

    def _validate_model(self, obj: Any, path: str = "") -> List[str]:
        """
        Model üzerindeki validation kurallarını kontrol eder.
        
        Args:
            obj: Validate edilecek model objesi.
            path: Hata mesajlarında kullanılacak alan yolu (nested objeler için).
        
        Returns:
            Hata mesajlarının listesi. Boş liste = geçerli model.
        """
        errors = []
        
        if obj is None:
            return errors
            
        # Liste ise elemanları validate et
        if isinstance(obj, list):
            for i, item in enumerate(obj):
                item_path = f"{path}[{i}]" if path else f"[{i}]"
                errors.extend(self._validate_model(item, item_path))
            return errors
        
        # _validation_rules dict'i varsa kontrol et
        if hasattr(obj, "_validation_rules") and isinstance(obj._validation_rules, dict):
            for field_name, rules in obj._validation_rules.items():
                field_path = f"{path}.{field_name}" if path else field_name
                value = getattr(obj, field_name, None)
                
                # Required kontrolü
                if rules.get("required", False) and (value is None or value == ""):
                    msg = rules.get("message", f"{field_path} alanı zorunludur.")
                    errors.append(msg)
                    continue
                
                # Pattern kontrolü (sadece değer varsa)
                pattern = rules.get("pattern")
                if pattern and value is not None and value != "":
                    if not re.match(pattern, str(value)):
                        msg = rules.get("message", f"{field_path} alanı geçersiz format.")
                        errors.append(msg)
        
        # İç içe objeleri validate et
        if hasattr(obj, "__dict__"):
            for attr_name, val in obj.__dict__.items():
                # Private alanları ve config_map/validation_rules'ı atla
                if attr_name.startswith("_"):
                    continue
                # Nested model veya liste ise recursive validate et
                if hasattr(val, "_validation_rules") or isinstance(val, list):
                    nested_path = f"{path}.{attr_name}" if path else attr_name
                    errors.extend(self._validate_model(val, nested_path))
        
        return errors

    def _unwrap_list(self, response: Any) -> Any:
        """{"result":[...]} sarmalı yanıtı listeye açar; değilse olduğu gibi döner.

        Liste dönen Resource metotları bunu kullanır (C# BaseResource ile aynı davranış).
        """
        if isinstance(response, dict) and "result" in response:
            return response["result"]
        return response

    def _debug_log(self, message: str, level: str = 'debug') -> None:
        """
        Enterprise logger veya debug moduna göre loglama yapar.
        
        Args:
            message: Yazdırılacak mesaj.
            level: Log seviyesi ('debug', 'warn', 'error').
        """

        if self.config.logger:
            if level == 'error':
                self.config.logger.error(f"[ODEAL SDK ERROR] {message}")
            elif level == 'warn':
                self.config.logger.warning(f"[ODEAL SDK WARN] {message}")
            else:
                self.config.logger.debug(f"[ODEAL SDK DEBUG] {message}")
        elif self.config.debug_mode or level == 'error':
            prefix = "[ODEAL SDK ERROR]" if level == 'error' else "[ODEAL SDK WARN]" if level == 'warn' else "[DEBUG]"
            print(f"{prefix} {message}")



    def _invoke_before_interceptors(self, method: str, url: str, headers: Dict[str, str], body: Optional[str] = None) -> None:
        """Interceptor'ların onBeforeRequest hook'unu çağırır."""
        if not hasattr(self.config, 'interceptors') or not self.config.interceptors:
            return
        req_ctx = RequestContext(
            method=method.upper(),
            url=url,
            headers=dict(headers),
            body=body
        )
        for interceptor in self.config.interceptors:
            interceptor.on_before_request(req_ctx)

    def _invoke_after_interceptors(self, method: str, url: str, headers: Dict[str, str], body: Optional[str], status_code: int, response_body: Optional[str], duration_ms: float) -> None:
        """Interceptor'ların onAfterResponse hook'unu çağırır."""
        if not hasattr(self.config, 'interceptors') or not self.config.interceptors:
            return
        req_ctx = RequestContext(
            method=method.upper(),
            url=url,
            headers=dict(headers),
            body=body
        )
        resp_ctx = ResponseContext(
            status_code=status_code,
            body=response_body,
            duration_ms=duration_ms,
            request=req_ctx
        )
        for interceptor in self.config.interceptors:
            interceptor.on_after_response(resp_ctx)

    def send_request(
        self,
        method: str,
        path: str,
        body: Any = None,
        query_params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        base_url: str = None
    ) -> Any:
        """
        HTTP isteği gönderir ve yanıtı döner.
        
        Args:
            method: HTTP metodu (GET, POST, PUT, DELETE vb.).
            path: API endpoint yolu.
            body: İstek gövdesi (opsiyonel).
            query_params: Query string parametreleri (opsiyonel).
            headers: Ek HTTP header'ları (opsiyonel).
            base_url: Alternatif base URL (opsiyonel).
        
        Returns:
            API yanıtı (JSON olarak deserialize edilmiş).
        
        Raises:
            OdealValidationException: Client-side validation başarısız olduğunda.
            OdealApiException: API isteği başarısız olduğunda.
        """
        # 1. Request Body'sini Config ile zenginleştir (Auto-Fill)
        if body is not None:
            self._fill_config_defaults(body)
        
        # 2. Client-side Validation (skip_client_validation False ise)
        if body is not None and not self.config.skip_client_validation:
            validation_errors = self._validate_model(body)
            if validation_errors:
                error_msg = "Validation hatası: " + "; ".join(validation_errors)
                self._debug_log(f"Validation Failed: {validation_errors}")
                raise OdealValidationException(error_msg, validation_errors)

        # 3. Base URL
        target_base_url = base_url if base_url else self.config.base_url
        target_base_url = target_base_url.rstrip('/')
        
        if not path.startswith('/'):
            path = '/' + path
            
        url = target_base_url + path

        # 4. Query Params
        if query_params:
            clean_params = {k: str(v) for k, v in query_params.items() if v is not None}
            if clean_params:
                url += '?' + urllib.parse.urlencode(clean_params)

        # 5. Headers - Swagger'dan gelen header parametreleri headers'tan gelir
        # BaseResource hardcoded header eklemez, tüm API header'ları Resource'dan gelir
        req_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-ODEAL-AGENT": self.AGENT
        }
        
        # Swagger'dan gelen header parametreleri (X-ODEAL-SECRET-KEY, X-ODEAL-MERCHANT-KEY vb.)
        # Bu header'lar Resource template'inde config'den doldurularak headers'a eklenir
        if headers:
            clean_headers = {k: str(v) for k, v in headers.items() if v is not None}
            req_headers.update(clean_headers)
        
        # Agent header'ını her zaman ez (Kullanıcı değiştiremesin)
        req_headers["X-ODEAL-AGENT"] = self.AGENT

        # OAuth2 / Bearer: access_token ayarlıysa Authorization header ekle (boşsa eklenmez)
        if getattr(self.config, 'access_token', None):
            req_headers["Authorization"] = f"Bearer {self.config.access_token}"


        # Idempotency Key: POST/PUT/PATCH isteklerinde çift işlem koruması
        if method.upper() in ('POST', 'PUT', 'PATCH'):
            idem_header = 'X-Odeal-Idempotency-Key'
            if idem_header not in req_headers:
                import uuid
                req_headers[idem_header] = uuid.uuid4().hex

        # 6. Body Serialization
        data_bytes = None
        json_str = None
        if isinstance(body, MultipartBody):
            # multipart/form-data: gövde baytları bir kez üretilir, Content-Type'ı ezilir.
            content_type, data_bytes = body.build()
            req_headers["Content-Type"] = content_type
        elif body is not None:
            try:
                payload = object_to_dict(body)
                json_str = json.dumps(payload)
                data_bytes = json_str.encode('utf-8')
                
                # Debug log - curl formatı
                if self.config.debug_mode:
                    curl_parts = [f"curl -X {method.upper()}"]
                    curl_parts.append(f"'{url}'")
                    for k, v in req_headers.items():
                        safe_val = v

                        if self.config.mask_sensitive_data and any(x in k.lower() for x in ['secret', 'key', 'authorization']):
                            safe_val = "***"
                        curl_parts.append(f"-H '{k}: {safe_val}'")
                    
                    safe_json_str = json_str

                    if self.config.mask_sensitive_data:
                        safe_json_str = sanitize_json(safe_json_str) or safe_json_str
                    curl_parts.append(f"-d '{safe_json_str}'")
                    self._debug_log(f"{' '.join(curl_parts)}")
                
            except Exception as e:
                raise OdealApiException(
                    message=f"Request Body Serialization Error: {str(e)}",
                    status_code=0
                )
        else:
            if self.config.debug_mode:
                curl_parts = [f"curl -X {method.upper()}"]
                curl_parts.append(f"'{url}'")
                for k, v in req_headers.items():
                    safe_val = v

                    if self.config.mask_sensitive_data and any(x in k.lower() for x in ['secret', 'key', 'authorization']):
                        safe_val = "***"
                    curl_parts.append(f"-H '{k}: {safe_val}'")
                self._debug_log(f"{' '.join(curl_parts)}")

        # 7. Request Gönderimi (Retry Logic ile)
        max_retries = self.config.max_retry_count if True else 0
        current_try = 0
        
        while True:
            # Circuit Breaker Guard
            if self._circuit_breaker and not self._circuit_breaker.allow_request():
                raise OdealCircuitOpenException()

            # Interceptor: onBeforeRequest
            self._invoke_before_interceptors(method, url, req_headers, json_str if body is not None else None)

            start_time = time.time()
            req = urllib.request.Request(url, data=data_bytes, method=method.upper())
            for k, v in req_headers.items():
                req.add_header(k, v)

            try:
                with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                    response_data = response.read()
                    duration_ms = (time.time() - start_time) * 1000
                    response_body_str = response_data.decode('utf-8') if response_data else None


                    # Interceptor: onAfterResponse
                    self._invoke_after_interceptors(method, url, req_headers, json_str if body is not None else None, response.status, response_body_str, duration_ms)

                    if not response_data:
                        self._debug_log(f"Response: (empty)")
                        return None
                        
                    result = json.loads(response_body_str)
                    self._debug_log(f"Response: {response_body_str[:500]}...")
                    if self._circuit_breaker:
                        self._circuit_breaker.record_success()
                    return result

            except urllib.error.HTTPError as e:
                duration_ms = (time.time() - start_time) * 1000
                try:
                    err_content = e.read().decode('utf-8')
                except:
                    err_content = str(e)


                # Interceptor: onAfterResponse (error case)
                self._invoke_after_interceptors(method, url, req_headers, json_str if body is not None else None, e.code, err_content, duration_ms)

                if self._circuit_breaker:
                    # Devre-kıran: 5xx/429 = başarısızlık; 4xx = sunucu yanıt verdi (başarı sayılır).
                    if e.code >= 500 or e.code == 429:
                        self._circuit_breaker.record_failure()
                    else:
                        self._circuit_breaker.record_success()

                # Sadece 5xx ve 429 için tekrar dene
                if e.code >= 500 or e.code == 429:
                    if current_try < max_retries:
                        current_try += 1
                        retry_after = e.headers.get('Retry-After')
                        try:
                            delay = int(retry_after) if retry_after else (2 ** current_try) * 0.5
                        except ValueError:
                            delay = (2 ** current_try) * 0.5
                        
                        self._debug_log(f"Request failed with HTTP {e.code}. Retrying in {delay}s. Attempt {current_try} of {max_retries}.", level='warn')
                        time.sleep(delay)
                        continue
                
                self._debug_log(f"HTTP Error {e.code}: {err_content}", level='error')
                # Zengin hata hiyerarşisi: status → spesifik exception tipi
                _exc_cls = {
                    401: OdealAuthenticationException, 403: OdealForbiddenException,
                    404: OdealNotFoundException, 429: OdealRateLimitException,
                }.get(e.code)
                if _exc_cls is not None:
                    raise _exc_cls(response_content=err_content)
                raise OdealApiException(f"HTTP {e.code}: {e.reason}", e.code, err_content)

            except urllib.error.URLError as e:
                # Ağ hatası / zaman aşımı = devre-kıran başarısızlığı
                if self._circuit_breaker:
                    self._circuit_breaker.record_failure()
                # Ağ hataları veya zaman aşımı için tekrar dene
                if current_try < max_retries:
                    current_try += 1
                    delay = (2 ** current_try) * 0.5
                    self._debug_log(f"Network Timeout/Error: {e.reason}. Retrying in {delay}s. Attempt {current_try} of {max_retries}.", level='warn')
                    time.sleep(delay)
                    continue
                    
                self._debug_log(f"Network Error: {e.reason}", level='error')
                raise OdealApiException(f"Network Error: {e.reason}", 0, str(e))

            except json.JSONDecodeError:
                raise OdealApiException("Invalid JSON Response", 200, "Response body could not be parsed as JSON.")
            except Exception as e:
                self._debug_log(f"Unexpected Error: {str(e)}", level='error')
                raise OdealApiException(f"Unexpected Error: {str(e)}", 0)

    async def send_request_async(
        self,
        method: str,
        path: str,
        body: Any = None,
        query_params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        base_url: str = None
    ) -> Any:
        """
        Asenkron HTTP isteği gönderir.
        
        sync send_request() metodunu asyncio.to_thread ile thread pool'a taşır.
        Event loop bloke olmaz, tüm retry/interceptor/circuit-breaker mantığı korunur.
        
        Args:
            method: HTTP metodu (GET, POST, PUT, DELETE vb.).
            path: API endpoint yolu.
            body: İstek gövdesi (opsiyonel).
            query_params: Query string parametreleri (opsiyonel).
            headers: Ek HTTP header'ları (opsiyonel).
            base_url: Alternatif base URL (opsiyonel).
        
        Returns:
            API yanıt verisi (dict / list / None).
        """
        return await asyncio.to_thread(
            self.send_request, method, path, body, query_params, headers, base_url
        )
