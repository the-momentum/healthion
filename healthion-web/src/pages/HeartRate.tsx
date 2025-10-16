import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import { Card, CardDescription, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useHeartRate } from "@/hooks/use-heart-rate";
import { useAuth } from "@/hooks/use-auth";
import { Skeleton } from "@/components/ui/skeleton";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function HeartRate() {
    const { isAuthenticated, isLoading } = useAuth();
    const [filters, setFilters] = useState({
        start_date: '',
        end_date: '',
        limit: 20
    });
    
    const { data: heartRateData, summary: heartRateSummary, meta: heartRateMeta, loading: heartRateLoading, refetch } = useHeartRate(filters);

    const handleFilterChange = (key: string, value: string) => {
        setFilters(prev => ({
            ...prev,
            [key]: value
        }));
    };

    const applyFilters = () => {
        refetch();
    };

    if (isLoading) {
        return (
            <>
                <PageHeader>
                    <PageHeaderHeading>Heart Rate Data</PageHeaderHeading>
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
                    <PageHeaderHeading>Heart Rate Data</PageHeaderHeading>
                </PageHeader>
                <Card>
                    <CardHeader>
                        <CardTitle>Access Denied</CardTitle>
                        <CardDescription>Please log in to view heart rate data.</CardDescription>
                    </CardHeader>
                </Card>
            </>
        );
    }

    return (
        <>
            <PageHeader>
                <PageHeaderHeading>Heart Rate Data</PageHeaderHeading>
            </PageHeader>
            
            {/* Filters */}
            <Card className="mb-6">
                <CardHeader>
                    <CardTitle>Filters</CardTitle>
                    <CardDescription>Filter your heart rate data by date range</CardDescription>
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
                            <label className="text-sm font-medium">Limit</label>
                            <Input
                                type="number"
                                value={filters.limit}
                                onChange={(e) => handleFilterChange('limit', e.target.value)}
                                min="1"
                                max="100"
                            />
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
            {heartRateSummary && (
                <Card className="mb-6">
                    <CardHeader>
                        <CardTitle>Summary</CardTitle>
                        <CardDescription>Statistical overview of your heart rate data</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div className="text-center">
                                <p className="text-3xl font-bold text-blue-600">{Math.round(heartRateSummary.avg_heart_rate)}</p>
                                <p className="text-sm text-muted-foreground">Average BPM</p>
                            </div>
                            <div className="text-center">
                                <p className="text-3xl font-bold text-green-600">{heartRateSummary.min_heart_rate}</p>
                                <p className="text-sm text-muted-foreground">Minimum BPM</p>
                            </div>
                            <div className="text-center">
                                <p className="text-3xl font-bold text-red-600">{heartRateSummary.max_heart_rate}</p>
                                <p className="text-sm text-muted-foreground">Maximum BPM</p>
                            </div>
                        </div>
                        {heartRateMeta && (
                            <div className="mt-4 text-center text-sm text-muted-foreground">
                                {heartRateMeta.result_count} measurements found
                            </div>
                        )}
                    </CardContent>
                </Card>
            )}

            {/* Data Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Heart Rate Measurements</CardTitle>
                    <CardDescription>Detailed view of your heart rate data</CardDescription>
                </CardHeader>
                <CardContent>
                    {heartRateLoading ? (
                        <div className="space-y-3">
                            {[...Array(5)].map((_, i) => (
                                <div key={i} className="flex justify-between items-center p-3 border rounded">
                                    <Skeleton className="h-4 w-20" />
                                    <Skeleton className="h-4 w-32" />
                                    <Skeleton className="h-4 w-24" />
                                </div>
                            ))}
                        </div>
                    ) : heartRateData.length > 0 ? (
                        <div className="space-y-2">
                            {heartRateData.map((measurement) => (
                                <div key={measurement.id} className="flex justify-between items-center p-3 border rounded hover:bg-muted/50">
                                    <div>
                                        <p className="font-medium">{Math.round(measurement.avg.value)} BPM</p>
                                        <p className="text-sm text-muted-foreground">
                                            {new Date(measurement.date).toLocaleString()}
                                        </p>
                                        <p className="text-xs text-muted-foreground">
                                            Range: {measurement.min.value}-{measurement.max.value} BPM
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-sm text-muted-foreground">
                                            ID: {measurement.id}
                                        </p>
                                        <p className="text-xs text-muted-foreground">
                                            {measurement.source}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-8">
                            <p className="text-muted-foreground">No heart rate data available</p>
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
