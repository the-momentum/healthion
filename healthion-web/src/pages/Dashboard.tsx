import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import { Card, CardDescription, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useAuth } from "@/hooks/use-auth";
import { useHeartRate } from "@/hooks/use-heart-rate";
import { useWorkouts } from "@/hooks/use-workouts";
import { Skeleton } from "@/components/ui/skeleton";
import { DebugPanel } from "@/components/debug-panel";

export default function Dashboard() {
    const { currentUser, isAuthenticated, isLoading } = useAuth();
    const { data: heartRateData, summary: heartRateSummary, meta: heartRateMeta, loading: heartRateLoading } = useHeartRate({ limit: 5 });
    const { data: workoutData, meta: workoutMeta, loading: workoutLoading } = useWorkouts({ 
        limit: 10,
        sort_by: 'startDate',
        sort_order: 'desc'
    });

    if (isLoading) {
        return (
            <>
                <PageHeader>
                    <PageHeaderHeading>Dashboard</PageHeaderHeading>
                </PageHeader>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    <Card>
                        <CardHeader>
                            <Skeleton className="h-4 w-32" />
                            <Skeleton className="h-3 w-48" />
                        </CardHeader>
                        <CardContent>
                            <Skeleton className="h-8 w-16" />
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader>
                            <Skeleton className="h-4 w-32" />
                            <Skeleton className="h-3 w-48" />
                        </CardHeader>
                        <CardContent>
                            <Skeleton className="h-8 w-16" />
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader>
                            <Skeleton className="h-4 w-32" />
                            <Skeleton className="h-3 w-48" />
                        </CardHeader>
                        <CardContent>
                            <Skeleton className="h-8 w-16" />
                        </CardContent>
                    </Card>
                </div>
            </>
        );
    }

    if (!isAuthenticated) {
        return (
            <>
                <PageHeader>
                    <PageHeaderHeading>Dashboard</PageHeaderHeading>
                </PageHeader>
                <Card>
                    <CardHeader>
                        <CardTitle>Welcome to Healthion</CardTitle>
                        <CardDescription>Please log in to view your health data.</CardDescription>
                    </CardHeader>
                </Card>
            </>
        );
    }

    return (
        <>
            <PageHeader>
                <PageHeaderHeading>Dashboard</PageHeaderHeading>
            </PageHeader>
            
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {/* User Info Card */}
                <Card>
                    <CardHeader>
                        <CardTitle>User Info</CardTitle>
                        <CardDescription>Your account information</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <p><strong>Email:</strong> {currentUser?.email}</p>
                            <p><strong>User ID:</strong> {currentUser?.user_id}</p>
                            <p><strong>Permissions:</strong> {currentUser?.permissions?.join(', ') || 'None'}</p>
                        </div>
                    </CardContent>
                </Card>

                {/* Heart Rate Card */}
                <Card>
                    <CardHeader>
                        <CardTitle>Heart Rate Summary</CardTitle>
                        <CardDescription>Your heart rate statistics</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {heartRateLoading ? (
                            <div className="space-y-2">
                                <Skeleton className="h-8 w-16" />
                                <Skeleton className="h-4 w-24" />
                                <Skeleton className="h-4 w-20" />
                            </div>
                        ) : heartRateSummary ? (
                            <div className="space-y-3">
                                <div className="grid grid-cols-3 gap-4 text-center">
                                    <div>
                                        <p className="text-2xl font-bold text-blue-600">{Math.round(heartRateSummary.avg_heart_rate)}</p>
                                        <p className="text-xs text-muted-foreground">Avg BPM</p>
                                    </div>
                                    <div>
                                        <p className="text-2xl font-bold text-green-600">{heartRateSummary.min_heart_rate}</p>
                                        <p className="text-xs text-muted-foreground">Min BPM</p>
                                    </div>
                                    <div>
                                        <p className="text-2xl font-bold text-red-600">{heartRateSummary.max_heart_rate}</p>
                                        <p className="text-xs text-muted-foreground">Max BPM</p>
                                    </div>
                                </div>
                                {heartRateMeta && (
                                    <p className="text-sm text-muted-foreground text-center">
                                        {heartRateMeta.result_count} measurements
                                    </p>
                                )}
                            </div>
                        ) : (
                            <p className="text-muted-foreground">No heart rate data available</p>
                        )}
                    </CardContent>
                </Card>

                {/* Workouts Card */}
                <Card>
                    <CardHeader>
                        <CardTitle>Recent Workouts</CardTitle>
                        <CardDescription>Your latest training sessions</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {workoutLoading ? (
                            <div className="space-y-2">
                                <Skeleton className="h-4 w-full" />
                                <Skeleton className="h-4 w-3/4" />
                                <Skeleton className="h-4 w-1/2" />
                            </div>
                        ) : workoutData.length > 0 ? (
                            <div className="space-y-2">
                                {workoutData.slice(0, 3).map((workout) => {
                                    // Convert duration to minutes for display
                                    const durationInSeconds = workout.durationUnit === 'min' ? workout.duration * 60 : 
                                                             workout.durationUnit === 'hr' ? workout.duration * 3600 : 
                                                             workout.duration;
                                    const durationInMinutes = Math.round(durationInSeconds / 60);
                                    
                                    return (
                                        <div key={workout.id} className="flex justify-between items-center">
                                            <div>
                                                <p className="font-medium">{workout.type || 'Unknown Workout'}</p>
                                                <p className="text-xs text-muted-foreground">
                                                    {new Date(workout.startDate).toLocaleString()}
                                                </p>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-sm font-medium">{durationInMinutes} min</p>
                                                <p className="text-xs text-muted-foreground">
                                                    {Math.round(workout.summary.total_calories || 0)} cal
                                                </p>
                                            </div>
                                        </div>
                                    );
                                })}
                                {workoutData.length > 3 && (
                                    <p className="text-xs text-muted-foreground text-center pt-2">
                                        +{workoutData.length - 3} more workouts
                                    </p>
                                )}
                                {workoutMeta && (
                                    <p className="text-xs text-muted-foreground text-center pt-2">
                                        {workoutMeta.result_count} total workouts
                                    </p>
                                )}
                            </div>
                        ) : (
                            <p className="text-muted-foreground">No workout data available</p>
                        )}
                    </CardContent>
                </Card>

                {/* Recent Heart Rate Measurements */}
                <Card>
                    <CardHeader>
                        <CardTitle>Recent Measurements</CardTitle>
                        <CardDescription>Latest heart rate readings</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {heartRateLoading ? (
                            <div className="space-y-2">
                                <Skeleton className="h-4 w-full" />
                                <Skeleton className="h-4 w-3/4" />
                                <Skeleton className="h-4 w-1/2" />
                            </div>
                        ) : heartRateData.length > 0 ? (
                            <div className="space-y-2">
                                {heartRateData.slice(0, 3).map((measurement, index) => (
                                    <div key={measurement.id} className="flex justify-between items-center">
                                        <div>
                                            <p className="font-medium">{Math.round(measurement.avg.value)} BPM</p>
                                            <p className="text-xs text-muted-foreground">
                                                {new Date(measurement.date).toLocaleString()}
                                            </p>
                                            <p className="text-xs text-muted-foreground">
                                                {measurement.min.value}-{measurement.max.value} BPM
                                            </p>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-sm text-muted-foreground">
                                                #{heartRateData.length - index}
                                            </p>
                                        </div>
                                    </div>
                                ))}
                                {heartRateData.length > 3 && (
                                    <p className="text-xs text-muted-foreground text-center pt-2">
                                        +{heartRateData.length - 3} more measurements
                                    </p>
                                )}
                            </div>
                        ) : (
                            <p className="text-muted-foreground">No recent measurements</p>
                        )}
                    </CardContent>
                </Card>
            </div>

            {/* Debug Panel */}
            <DebugPanel />
        </>
    );
}
