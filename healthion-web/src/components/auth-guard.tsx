import { ReactNode } from 'react'
import { useAuth } from '@/hooks/use-auth'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

interface AuthGuardProps {
  children: ReactNode
  fallback?: ReactNode
}

export const AuthGuard = ({ children, fallback }: AuthGuardProps) => {
  const { isAuthenticated, isLoading, login } = useAuth()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="space-y-4 w-full max-w-md">
          <Skeleton className="h-8 w-3/4" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-2/3" />
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    if (fallback) {
      return <>{fallback}</>
    }

    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <CardTitle>Authentication Required</CardTitle>
            <CardDescription>
              Please sign in to access this page.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <Button onClick={login} className="w-full">
              Sign In
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return <>{children}</>
}
