import { useState, useEffect } from 'react'
import { apiService, WorkoutData, WorkoutFilters, WorkoutMeta } from '../lib/api'
import { useAuth } from './use-auth'

export const useWorkouts = (filters?: WorkoutFilters) => {
  const { getAccessToken, isAuthenticated } = useAuth()
  const [data, setData] = useState<WorkoutData[]>([])
  const [meta, setMeta] = useState<WorkoutMeta | null>(null)
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

      const response = await apiService.getWorkouts(token, filters)
      setData(response.data.data)
      setMeta(response.data.meta)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch workouts data')
      console.error('Error fetching workouts data:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [isAuthenticated, filters?.start_date, filters?.end_date, filters?.limit, filters?.offset])

  return {
    data,
    meta,
    loading,
    error,
    refetch: fetchData,
  }
}
