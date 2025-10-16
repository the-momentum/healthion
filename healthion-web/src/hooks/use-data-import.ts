import { useState } from 'react'
import { apiService } from '../lib/api'
import { useAuth } from './use-auth'

export const useDataImport = () => {
  const { getAccessToken, isAuthenticated } = useAuth()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const importData = async (file: File) => {
    if (!isAuthenticated) {
      setError('User not authenticated')
      return false
    }

    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const token = await getAccessToken()
      if (!token) {
        throw new Error('No access token available')
      }

      console.log('📤 Importing file:', {
        name: file.name,
        size: file.size,
        type: file.type,
        token: token.substring(0, 20) + '...'
      })

      const response = await apiService.importData(token, file)
      console.log('📦 Import response:', response)
      setSuccess(true)
      return true
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to import data'
      setError(errorMessage)
      console.error('❌ Error importing data:', err)
      return false
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setError(null)
    setSuccess(false)
  }

  return {
    importData,
    loading,
    error,
    success,
    reset,
  }
}
