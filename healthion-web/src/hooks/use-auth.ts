import { useAuth0 } from '@auth0/auth0-react'

export const useAuth = () => {
  const {
    user,
    isAuthenticated,
    isLoading,
    loginWithRedirect,
    logout,
    getAccessTokenSilently,
    getIdTokenClaims,
  } = useAuth0()

  const login = () => {
    loginWithRedirect()
  }

  const logoutUser = () => {
    logout({
      logoutParams: {
        returnTo: window.location.origin,
      },
    })
  }

  const getAccessToken = async () => {
    try {
      return await getAccessTokenSilently()
    } catch (error) {
      console.error('Error getting access token:', error)
      return null
    }
  }

  const getIdToken = async () => {
    try {
      const claims = await getIdTokenClaims()
      return claims?.__raw
    } catch (error) {
      console.error('Error getting ID token:', error)
      return null
    }
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout: logoutUser,
    getAccessToken,
    getIdToken,
  }
}
