import { useAuth0 } from '@auth0/auth0-react'
import { apiService, User } from '../lib/api'
import { useState, useEffect } from 'react'

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

  const [currentUser, setCurrentUser] = useState<User | null>(null)
  const [isLoadingUser, setIsLoadingUser] = useState(false)

  // Fetch current user data when authenticated
  useEffect(() => {
    const fetchCurrentUser = async () => {
      if (isAuthenticated && !isLoading) {
        setIsLoadingUser(true)
        try {
          const token = await getAccessTokenSilently()
          const response = await apiService.getCurrentUser(token)
          setCurrentUser(response.data)
        } catch (error) {
          console.error('Error fetching current user:', error)
          setCurrentUser(null)
        } finally {
          setIsLoadingUser(false)
        }
      } else {
        setCurrentUser(null)
      }
    }

    fetchCurrentUser()
  }, [isAuthenticated, isLoading, getAccessTokenSilently])

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
    currentUser,
    isAuthenticated,
    isLoading: isLoading || isLoadingUser,
    login,
    logout: logoutUser,
    getAccessToken,
    getIdToken,
  }
}
