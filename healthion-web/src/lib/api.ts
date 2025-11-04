import { appConfig } from '../config/app'

export interface ApiResponse<T = any> {
  data: T
  message?: string
  error?: string
}

export interface User {
  user_id: string
  email: string
  permissions: string[]
}

export interface HeartRateData {
  id: number
  workout_id: string
  date: string
  source: string
  units: string
  avg: {
    value: number
    unit: string
  }
  min: {
    value: number
    unit: string
  }
  max: {
    value: number
    unit: string
  }
}

export interface HeartRateRecoveryData {
  id: number
  workout_id: string
  date: string
  source: string
  units: string
  avg: {
    value: number
    unit: string
  }
  min: {
    value: number
    unit: string
  }
  max: {
    value: number
    unit: string
  }
}

export interface HeartRateSummary {
  total_records: number
  avg_heart_rate: number
  max_heart_rate: number
  min_heart_rate: number
  avg_recovery_rate: number
  max_recovery_rate: number
  min_recovery_rate: number
}

export interface HeartRateMeta {
  requested_at: string
  filters: {
    sort_by: string
    sort_order: string
    limit: number
    offset: number
  }
  result_count: number
  date_range: {
    start: string
    end: string
  }
}

export interface HeartRateResponse {
  data: HeartRateData[]
  recovery_data: HeartRateRecoveryData[]
  summary: HeartRateSummary
  meta: HeartRateMeta
}

export interface WorkoutData {
  id: string
  type: string | null
  startDate: string
  endDate: string
  duration: number
  durationUnit: string
  sourceName: string | null
  user_id: string
  summary: WorkoutSummary
}

export interface WorkoutSummary {
  total_statistics: number
  avg_statistic_value: number
  max_statistic_value: number
  min_statistic_value: number
  avg_heart_rate: number
  max_heart_rate: number
  min_heart_rate: number
  total_calories: number
}

export interface WorkoutMeta {
  requested_at: string
  result_count: number
}

export interface WorkoutResponse {
  data: WorkoutData[]
  meta: WorkoutMeta
}

export interface HeartRateFilters {
  start_date?: string
  end_date?: string
  limit?: number
  offset?: number
}

export interface WorkoutFilters {
  start_date?: string
  end_date?: string
  limit?: number
  offset?: number
  workout_type?: string
  location?: 'Indoor' | 'Outdoor'
  min_duration?: number
  max_duration?: number
  min_distance?: number
  max_distance?: number
  sort_by?: 'startDate' | 'endDate' | 'duration' | 'type' | 'sourceName'
  sort_order?: 'asc' | 'desc'
}

class ApiService {
  private baseUrl: string

  constructor() {
    this.baseUrl = appConfig.api.baseUrl
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {},
    token?: string
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`
    
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string>),
    }

    // Only set Content-Type if not already set (for FormData, browser sets it automatically)
    if (!headers['Content-Type'] && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json'
    }

    if (token) {
      headers.Authorization = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { data }
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // User endpoints
  async getCurrentUser(token: string): Promise<ApiResponse<User>> {
    return this.makeRequest<User>('/me', {
      method: 'GET',
    }, token)
  }

  // Heart rate endpoints
  async getHeartRateData(
    token: string,
    filters?: HeartRateFilters
  ): Promise<ApiResponse<HeartRateResponse>> {
    const queryParams = new URLSearchParams()
    
    if (filters?.start_date) queryParams.append('start_date', filters.start_date)
    if (filters?.end_date) queryParams.append('end_date', filters.end_date)
    if (filters?.limit) queryParams.append('limit', filters.limit.toString())
    if (filters?.offset) queryParams.append('offset', filters.offset.toString())

    const queryString = queryParams.toString()
    const endpoint = queryString ? `/heart-rate?${queryString}` : '/heart-rate'

    return this.makeRequest<HeartRateResponse>(endpoint, {
      method: 'GET',
    }, token)
  }

  // Workout endpoints
  async getWorkouts(
    token: string,
    filters?: WorkoutFilters
  ): Promise<ApiResponse<WorkoutResponse>> {
    const queryParams = new URLSearchParams()
    
    // Basic filters
    if (filters?.start_date) queryParams.append('start_date', filters.start_date)
    if (filters?.end_date) queryParams.append('end_date', filters.end_date)
    if (filters?.limit) queryParams.append('limit', filters.limit.toString())
    if (filters?.offset) queryParams.append('offset', filters.offset.toString())
    
    // Workout specific filters
    if (filters?.workout_type) queryParams.append('workout_type', filters.workout_type)
    if (filters?.location) queryParams.append('location', filters.location)
    if (filters?.min_duration) queryParams.append('min_duration', filters.min_duration.toString())
    if (filters?.max_duration) queryParams.append('max_duration', filters.max_duration.toString())
    if (filters?.min_distance) queryParams.append('min_distance', filters.min_distance.toString())
    if (filters?.max_distance) queryParams.append('max_distance', filters.max_distance.toString())
    if (filters?.sort_by) queryParams.append('sort_by', filters.sort_by)
    if (filters?.sort_order) queryParams.append('sort_order', filters.sort_order)

    const queryString = queryParams.toString()
    const endpoint = queryString ? `/workouts?${queryString}` : '/workouts'

    return this.makeRequest<WorkoutResponse>(endpoint, {
      method: 'GET',
    }, token)
  }

  // Import data endpoint
  async importData(token: string, file: File): Promise<ApiResponse> {
    const formData = new FormData()
    formData.append('file', file)

    return this.makeRequest('/import-data', {
      method: 'POST',
      body: formData,
    }, token)
  }
}

export const apiService = new ApiService()
