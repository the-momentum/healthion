import { useAuth } from '@/hooks/use-auth'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Separator } from '@/components/ui/separator'

export default function Profile() {
  const { user, isAuthenticated } = useAuth()

  if (!isAuthenticated || !user) {
    return null
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Profile</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Personal Information</CardTitle>
          <CardDescription>
            Your profile information from Auth0
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center space-x-4">
            <Avatar className="h-20 w-20">
              <AvatarImage src={user.picture} alt={user.name} />
              <AvatarFallback className="text-lg">
                {user.name?.charAt(0)?.toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div className="space-y-1">
              <h3 className="text-2xl font-semibold">{user.name}</h3>
              <p className="text-sm text-muted-foreground">{user.email}</p>
              {user.email_verified && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                  Verified Email
                </span>
              )}
            </div>
          </div>

          <Separator />

          <div className="grid gap-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-muted-foreground">
                  User ID
                </label>
                <p className="text-sm font-mono break-all">{user.sub}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-muted-foreground">
                  Updated At
                </label>
                <p className="text-sm">
                  {user.updated_at ? new Date(user.updated_at).toLocaleDateString() : 'N/A'}
                </p>
              </div>
            </div>

            {user.nickname && (
              <div>
                <label className="text-sm font-medium text-muted-foreground">
                  Nickname
                </label>
                <p className="text-sm">{user.nickname}</p>
              </div>
            )}

            {user.locale && (
              <div>
                <label className="text-sm font-medium text-muted-foreground">
                  Locale
                </label>
                <p className="text-sm">{user.locale}</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
