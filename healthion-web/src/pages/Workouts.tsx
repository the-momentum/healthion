import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import { Card, CardDescription, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useWorkouts } from "@/hooks/use-workouts";
import { useAuth } from "@/hooks/use-auth";
import { Skeleton } from "@/components/ui/skeleton";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function Workouts() {
    const { isAuthenticated, isLoading } = useAuth();
    const [filters, setFilters] = useState({
        start_date: '',
        end_date: '',
        limit: 20,
        workout_type: '',
        location: undefined as 'Indoor' | 'Outdoor' | undefined,
        sort_by: 'date' as 'date' | 'duration' | 'distance' | 'calories',
        sort_order: 'desc' as 'asc' | 'desc'
    });
    
    const { data: workoutData, meta: workoutMeta, loading: workoutLoading, error: workoutError, refetch } = useWorkouts(filters);

    const handleFilterChange = (key: string, value: string) => {
        setFilters(prev => ({
            ...prev,
            [key]: key === 'location' ? (value === '' ? undefined : value as 'Indoor' | 'Outdoor') :
                   key === 'sort_by' ? value as 'date' | 'duration' | 'distance' | 'calories' :
                   key === 'sort_order' ? value as 'asc' | 'desc' :
                   key === 'limit' ? parseInt(value) || 20 :
                   value
        }));
    };

    const applyFilters = () => {
        refetch();
    };

    if (isLoading) {
        return (
            <>
                <PageHeader>
                    <PageHeaderHeading>Workouts</PageHeaderHeading>
                </PageHeader>
                <div className="space-y-4">
                    <Card>
                        <CardHeader>
                            <Skeleton className="h-6 w-48" />
                            <Skeleton className="h-4 w-64" />
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-3 gap-4">
                                <Skeleton className="h-16 w-full" />
                                <Skeleton className="h-16 w-full" />
                                <Skeleton className="h-16 w-full" />
                            </div>
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
                    <PageHeaderHeading>Workouts</PageHeaderHeading>
                </PageHeader>
                <Card>
                    <CardHeader>
                        <CardTitle>Access Denied</CardTitle>
                        <CardDescription>Please log in to view workout data.</CardDescription>
                    </CardHeader>
                </Card>
            </>
        );
    }

    return (
        <>
            <PageHeader>
                <PageHeaderHeading>Workouts</PageHeaderHeading>
            </PageHeader>
            
            {/* Filters */}
            <Card className="mb-6">
                <CardHeader>
                    <CardTitle>Filters</CardTitle>
                    <CardDescription>Filter your workout data</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div>
                            <label className="text-sm font-medium">Start Date</label>
                            <Input
                                type="date"
                                value={filters.start_date}
                                onChange={(e) => handleFilterChange('start_date', e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="text-sm font-medium">End Date</label>
                            <Input
                                type="date"
                                value={filters.end_date}
                                onChange={(e) => handleFilterChange('end_date', e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="text-sm font-medium">Workout Type</label>
                            <Input
                                type="text"
                                placeholder="e.g. Outdoor Walk"
                                value={filters.workout_type}
                                onChange={(e) => handleFilterChange('workout_type', e.target.value)}
                            />
                        </div>
                        <div>
                            <label className="text-sm font-medium">Location</label>
                            <Select value={filters.location || 'all'} onValueChange={(value) => handleFilterChange('location', value === 'all' ? '' : value)}>
                                <SelectTrigger>
                                    <SelectValue placeholder="All locations" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all">All locations</SelectItem>
                                    <SelectItem value="Indoor">Indoor</SelectItem>
                                    <SelectItem value="Outdoor">Outdoor</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <label className="text-sm font-medium">Limit</label>
                            <Input
                                type="number"
                                value={filters.limit}
                                onChange={(e) => handleFilterChange('limit', e.target.value)}
                                min="1"
                                max="100"
                            />
                        </div>
                        <div>
                            <label className="text-sm font-medium">Sort By</label>
                            <Select value={filters.sort_by} onValueChange={(value) => handleFilterChange('sort_by', value)}>
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="date">Date</SelectItem>
                                    <SelectItem value="duration">Duration</SelectItem>
                                    <SelectItem value="distance">Distance</SelectItem>
                                    <SelectItem value="calories">Calories</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <label className="text-sm font-medium">Sort Order</label>
                            <Select value={filters.sort_order} onValueChange={(value) => handleFilterChange('sort_order', value)}>
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="desc">Descending</SelectItem>
                                    <SelectItem value="asc">Ascending</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="flex items-end">
                            <Button onClick={applyFilters} className="w-full">
                                Apply Filters
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Summary */}
            {workoutMeta && (
                <Card className="mb-6">
                    <CardHeader>
                        <CardTitle>Summary</CardTitle>
                        <CardDescription>Statistical overview of your workouts</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div className="text-center">
                                <p className="text-3xl font-bold text-purple-600">{workoutMeta.result_count}</p>
                                <p className="text-sm text-muted-foreground">Total Workouts</p>
                            </div>
                            <div className="text-center">
                                <p className="text-3xl font-bold text-orange-600">
                                    {Math.round(workoutData.reduce((sum, w) => sum + w.duration, 0) / 60)}
                                </p>
                                <p className="text-sm text-muted-foreground">Total Minutes</p>
                            </div>
                            <div className="text-center">
                                <p className="text-3xl font-bold text-green-600">
                                    {Math.round(workoutData.reduce((sum, w) => sum + (w.active_energy_burned.value * 0.239), 0))}
                                </p>
                                <p className="text-sm text-muted-foreground">Total Calories</p>
                            </div>
                        </div>
                        <div className="mt-4 text-center text-sm text-muted-foreground">
                            {workoutMeta.result_count} workouts found
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Data Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Workouts</CardTitle>
                    <CardDescription>Your workout sessions</CardDescription>
                </CardHeader>
                <CardContent>
                    {workoutError ? (
                        <div className="text-center py-8">
                            <p className="text-red-600 font-medium">Error loading workout data</p>
                            <p className="text-sm text-muted-foreground mt-2">{workoutError}</p>
                            <Button onClick={refetch} className="mt-4">
                                Try Again
                            </Button>
                        </div>
                    ) : workoutLoading ? (
                        <div className="space-y-3">
                            {[...Array(5)].map((_, i) => (
                                <div key={i} className="flex justify-between items-center p-3 border rounded">
                                    <Skeleton className="h-4 w-20" />
                                    <Skeleton className="h-4 w-32" />
                                    <Skeleton className="h-4 w-24" />
                                </div>
                            ))}
                        </div>
                    ) : workoutData.length > 0 ? (
                        <div className="space-y-2">
                            {workoutData.map((workout) => (
                                <div key={workout.id} className="flex justify-between items-center p-3 border rounded hover:bg-muted/50">
                                    <div>
                                        <p className="font-medium">{workout.name}</p>
                                        <p className="text-sm text-muted-foreground">
                                            {new Date(workout.start).toLocaleString()}
                                        </p>
                                        <p className="text-xs text-muted-foreground">
                                            {workout.location} • {workout.distance.value.toFixed(2)} {workout.distance.unit}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-sm font-medium">{Math.round(workout.duration / 60)} min</p>
                                        <p className="text-sm text-muted-foreground">
                                            {Math.round(workout.active_energy_burned.value * 0.239)} cal
                                        </p>
                                        <p className="text-xs text-muted-foreground">
                                            HR: {Math.round(workout.summary.avg_heart_rate)} bpm
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-8">
                            <p className="text-muted-foreground">No workout data available</p>
                            <p className="text-sm text-muted-foreground mt-2">
                                Try adjusting your filters or import some data
                            </p>
                        </div>
                    )}
                </CardContent>
            </Card>
        </>
    );
}
