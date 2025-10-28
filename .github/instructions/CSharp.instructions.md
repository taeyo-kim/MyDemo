# C# Instructions

## Coding Style
- 클래스/메서드/속성: **PascalCase**
- 지역 변수/매개변수: **camelCase**
- 비동기 메서드는 **Async** 접미사 사용 (예: `GetUserAsync`)
- `var`는 **명확한 타입 추론**이 가능한 경우에만 사용

## Architecture & Patterns
- DI 컨테이너 사용 (예: `Microsoft.Extensions.DependencyInjection`)  
- 비즈니스 로직은 **Service/Domain** 계층에, 데이터 접근은 **Repository** 계층에
- 로깅은 `ILogger<T>`로 일관성 유지, **예외 처리**는 상위 계층에서 집약

## Async & Resource Management
- I/O 바운드 작업은 **`async/await`** 우선
- 리소스 해제는 `using` 또는 `IAsyncDisposable`을 활용
- ConfigureAwait는 **라이브러리 코드**에서만 `false` 고려

## Testing (applyTo: tests/**)
- **xUnit** 사용, 테스트 메서드명은 `MethodName_Should_ExpectedBehavior`
- **AAA(Arrange-Act-Assert)** 패턴 유지, **FluentAssertions** 권장
- **Mocking**은 `Moq` 사용, 외부 의존성은 **Stub/Mock**으로 격리

## Security
- 하드코딩된 시크릿 금지: **`IConfiguration`/User Secrets/Key Vault**
- 입력 검증: Model Validation + Guard Clauses
- 외부 API 호출 시 **타임아웃/재시도/서킷브레이커**(Polly) 적용

