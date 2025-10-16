import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Auth0Provider } from '@auth0/auth0-react'
import './index.css'
import App from './App.tsx'
import { appConfig } from './config/app'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Auth0Provider
      domain={appConfig.auth0.domain}
      clientId={appConfig.auth0.clientId}
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: appConfig.auth0.audience,
        scope: 'openid profile email'
      }}
      useRefreshTokens={true}
      cacheLocation="localstorage"
    >
      <App />
    </Auth0Provider>
  </StrictMode>,
)
