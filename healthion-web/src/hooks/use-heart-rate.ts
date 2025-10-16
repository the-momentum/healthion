import { useState, useEffect } from 'react'
import { apiService, HeartRateData, HeartRateRecoveryData, HeartRateFilters, HeartRateSummary, HeartRateMeta } from '../lib/api'
import { useAuth } from './use-auth'

export const useHeartRate = (filters?: HeartRateFilters) => {
  const { getAccessToken, isAuthenticated } = useAuth()
  const [data, setData] = useState<HeartRateData[]>([])
  const [recoveryData, setRecoveryData] = useState<HeartRateRecoveryData[]>([])
  const [summary, setSummary] = useState<HeartRateSummary | null>(null)
  const [meta, setMeta] = useState<HeartRateMeta | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    if (!isAuthenticated) return

    setLoading(true)
    setError(null)

    try {
      const token = await getAccessToken()
      if (!token) {
        throw new Error('No access token available')
      }

      const response = await apiService.getHeartRateData(token, filters)
      setData(response.data.data)
      setRecoveryData(response.data.recovery_data)
      setSummary(response.data.summary)
      setMeta(response.data.meta)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch heart rate data')
      console.error('Error fetching heart rate data:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [isAuthenticated, filters?.start_date, filters?.end_date, filters?.limit, filters?.offset])

  return {
    data,
    recoveryData,
    summary,
    meta,
    loading,
    error,
    refetch: fetchData,
  }
}
