import { useState } from 'react'
import { useAuth } from '@/hooks/use-auth'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { ChevronDown, ChevronRight, Copy, Check } from 'lucide-react'

export const DebugPanel = () => {
  const { user, currentUser, isAuthenticated, isLoading, getAccessToken, getIdToken } = useAuth()
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [idToken, setIdToken] = useState<string | null>(null)
  const [copied, setCopied] = useState<string | null>(null)
  const [isOpen, setIsOpen] = useState(false)

  const handleGetTokens = async () => {
    try {
      const token = await getAccessToken()
      const idTokenValue = await getIdToken()
      setAccessToken(token)
      setIdToken(idTokenValue ?? null)
    } catch (error) {
      console.error('Error getting tokens:', error)
    }
  }

  const copyToClipboard = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(type)
      setTimeout(() => setCopied(null), 2000)
    } catch (error) {
      console.error('Failed to copy:', error)
    }
  }

  if (!isAuthenticated) {
    return null
  }

  return (
    <Card className="mt-6 border-2 border-blue-200 bg-blue-50 dark:bg-blue-950 dark:border-blue-800">
      <Collapsible open={isOpen} onOpenChange={setIsOpen}>
        <CollapsibleTrigger asChild>
          <CardHeader className="cursor-pointer hover:bg-blue-100 dark:hover:bg-blue-900 transition-colors">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-blue-800 dark:text-blue-200">🐛 Debug Panel</CardTitle>
                <CardDescription className="text-blue-600 dark:text-blue-300">Auth0 and API debugging information</CardDescription>
              </div>
              {isOpen ? <ChevronDown className="h-4 w-4 text-blue-800 dark:text-blue-200" /> : <ChevronRight className="h-4 w-4 text-blue-800 dark:text-blue-200" />}
            </div>
          </CardHeader>
        </CollapsibleTrigger>
        <CollapsibleContent>
          <CardContent className="space-y-4">
            {/* Auth0 User Data */}
            <div>
              <h4 className="font-semibold mb-2 text-gray-800 dark:text-gray-200">Auth0 User Data:</h4>
              <pre className="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 p-3 rounded text-xs overflow-auto max-h-32 text-gray-800 dark:text-gray-200">
                {JSON.stringify(user, null, 2)}
              </pre>
            </div>

            {/* Current User from API */}
            <div>
              <h4 className="font-semibold mb-2 text-gray-800 dark:text-gray-200">Current User (from API):</h4>
              <pre className="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 p-3 rounded text-xs overflow-auto max-h-32 text-gray-800 dark:text-gray-200">
                {JSON.stringify(currentUser, null, 2)}
              </pre>
            </div>

            {/* Loading States */}
            <div>
              <h4 className="font-semibold mb-2 text-gray-800 dark:text-gray-200">Loading States:</h4>
              <div className="grid grid-cols-2 gap-2 text-sm text-gray-700 dark:text-gray-300">
                <div>isAuthenticated: <span className="font-mono text-green-600 dark:text-green-400">{String(isAuthenticated)}</span></div>
                <div>isLoading: <span className="font-mono text-blue-600 dark:text-blue-400">{String(isLoading)}</span></div>
              </div>
            </div>

            {/* Tokens */}
            <div>
              <h4 className="font-semibold mb-2 text-gray-800 dark:text-gray-200">Tokens:</h4>
              <div className="space-y-2">
                <Button onClick={handleGetTokens} size="sm" variant="outline">
                  Get Tokens
                </Button>
                
                {accessToken && (
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Access Token:</span>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => copyToClipboard(accessToken, 'access')}
                      >
                        {copied === 'access' ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                      </Button>
                    </div>
                    <pre className="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 p-2 rounded text-xs overflow-auto max-h-20 text-gray-800 dark:text-gray-200">
                      {accessToken}
                    </pre>
                  </div>
                )}

                {idToken && (
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">ID Token:</span>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => copyToClipboard(idToken, 'id')}
                      >
                        {copied === 'id' ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                      </Button>
                    </div>
                    <pre className="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 p-2 rounded text-xs overflow-auto max-h-20 text-gray-800 dark:text-gray-200">
                      {idToken}
                    </pre>
                  </div>
                )}
              </div>
            </div>

            {/* API Test */}
            <div>
              <h4 className="font-semibold mb-2 text-gray-800 dark:text-gray-200">API Test:</h4>
              <div className="space-y-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={async () => {
                    try {
                      const token = await getAccessToken()
                      if (token) {
                        console.log('🔍 Testing /api/v1/me with token:', token.substring(0, 20) + '...')
                        const response = await fetch('http://localhost:8000/api/v1/me', {
                          headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                          }
                        })
                        console.log('📡 Response status:', response.status)
                        const data = await response.json()
                        console.log('📦 API Response:', data)
                        alert(`API Response: ${JSON.stringify(data, null, 2)}`)
                      }
                    } catch (error) {
                      console.error('❌ API Test Error:', error)
                      alert(`API Error: ${error}`)
                    }
                  }}
                >
                  Test /api/v1/me
                </Button>
                
                <Button
                  size="sm"
                  variant="outline"
                  onClick={async () => {
                    try {
                      const token = await getAccessToken()
                      if (token) {
                        console.log('🔍 Testing /api/v1/heart-rate with token:', token.substring(0, 20) + '...')
                        const response = await fetch('http://localhost:8000/api/v1/heart-rate', {
                          headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                          }
                        })
                        console.log('📡 Response status:', response.status)
                        const data = await response.json()
                        console.log('📦 Heart Rate Response:', data)
                        alert(`Heart Rate Response: ${JSON.stringify(data, null, 2)}`)
                      }
                    } catch (error) {
                      console.error('❌ Heart Rate Test Error:', error)
                      alert(`Heart Rate Error: ${error}`)
                    }
                  }}
                >
                  Test /api/v1/heart-rate
                </Button>
                
                <Button
                  size="sm"
                  variant="outline"
                  onClick={async () => {
                    try {
                      const token = await getAccessToken()
                      if (token) {
                        console.log('🔍 Testing /api/v1/workouts with token:', token.substring(0, 20) + '...')
                        const response = await fetch('http://localhost:8000/api/v1/workouts?limit=5&sort_by=date&sort_order=desc', {
                          headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                          }
                        })
                        console.log('📡 Response status:', response.status)
                        const data = await response.json()
                        console.log('📦 Workouts Response:', data)
                        alert(`Workouts Response: ${JSON.stringify(data, null, 2)}`)
                      }
                    } catch (error) {
                      console.error('❌ Workouts Test Error:', error)
                      alert(`Workouts Error: ${error}`)
                    }
                  }}
                >
                  Test /api/v1/workouts
                </Button>
              </div>
            </div>
          </CardContent>
        </CollapsibleContent>
      </Collapsible>
    </Card>
  )
}
