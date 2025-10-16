import { PageHeader, PageHeaderHeading } from "@/components/page-header";
import { Card, CardDescription, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useDataImport } from "@/hooks/use-data-import";
import { useAuth } from "@/hooks/use-auth";
import { useState, useRef } from "react";
import { appConfig } from "@/config/app";

export default function ImportData() {
    const { isAuthenticated, isLoading, getAccessToken } = useAuth();
    const { importData, loading, error, success, reset } = useDataImport();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [authToken, setAuthToken] = useState<string>("");
    const [showToken, setShowToken] = useState<boolean>(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setSelectedFile(file);
            reset(); // Reset previous states
        }
    };

    const handleImport = async () => {
        if (!selectedFile) return;

        const success = await importData(selectedFile);
        if (success) {
            setSelectedFile(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    // TODO: Implement a way to generate long-lived, properly scoped token for the user
    const handleGenerateToken = async () => {
        try {
            const token = await getAccessToken();
            setAuthToken(token || "");
            setShowToken(true);
        } catch (error) {
            console.error("Failed to generate token:", error);
        }
    };

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
    };

    if (isLoading) {
        return (
            <>
                <PageHeader>
                    <PageHeaderHeading>Connect your data</PageHeaderHeading>
                </PageHeader>
                <Card>
                    <CardHeader>
                        <CardTitle>Loading...</CardTitle>
                    </CardHeader>
                </Card>
            </>
        );
    }

    if (!isAuthenticated) {
        return (
            <>
                <PageHeader>
                    <PageHeaderHeading>Connect your data</PageHeaderHeading>
                </PageHeader>
                <Card>
                    <CardHeader>
                        <CardTitle>Access Denied</CardTitle>
                        <CardDescription>Please log in to connect your data.</CardDescription>
                    </CardHeader>
                </Card>
            </>
        );
    }

    return (
        <>
            <PageHeader>
                <PageHeaderHeading>Connect your data</PageHeaderHeading>
            </PageHeader>

            <Tabs defaultValue="apple-health" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="apple-health">Apple Health</TabsTrigger>
                    <TabsTrigger value="mcp">MCP</TabsTrigger>
                </TabsList>

                <TabsContent value="apple-health" className="space-y-6">
                    {/* Apple Health Sync Card */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Sync Apple Health data</CardTitle>
                            <CardDescription>
                                Set up continuous synchronization of your Apple Health data.
                            </CardDescription>
                            <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-md">
                                <p className="text-sm text-blue-800">
                                    <strong>💡 Best for always-updated data:</strong> mobile app of your choice automatically syncs your health data in the background, ensuring you always have the latest information without manual intervention.
                                </p>
                            </div>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <p className="text-sm font-medium">API Endpoint:</p>
                                <div className="flex items-center gap-2">
                                    <code className="flex-1 p-2 bg-muted rounded text-sm font-mono">
                                        {appConfig.api.baseUrl}/import_data
                                    </code>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => copyToClipboard(`${appConfig.api.baseUrl}/import_data`)}
                                    >
                                        Copy
                                    </Button>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <p className="text-sm font-medium">Authentication Token:</p>
                                <div className="flex gap-2">
                                    <Button
                                        onClick={handleGenerateToken}
                                        variant="outline"
                                    >
                                        Generate Token
                                    </Button>
                                    {showToken && authToken && (
                                        <>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => copyToClipboard(authToken)}
                                            >
                                                Copy Token
                                            </Button>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => setShowToken(false)}
                                            >
                                                Hide
                                            </Button>
                                        </>
                                    )}
                                </div>
                                {showToken && authToken && (
                                    <div className="p-2 bg-muted rounded text-xs font-mono break-all">
                                        {authToken}
                                    </div>
                                )}
                            </div>

                            <div className="space-y-2">
                                <p className="text-sm font-medium">Instructions for mobile app:</p>
                                <div className="text-sm text-muted-foreground space-y-1">
                                    <p>1. Download a health data export app (e.g., <a href="https://apps.apple.com/us/app/health-auto-export-json-csv/id1115567069" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">Health Auto Export</a> or similar)</p>
                                    <p>2. Configure the app to send data to the endpoint above</p>
                                    <p>3. Use the authentication token in the Authorization header</p>
                                    <p>4. Set up automatic sync schedule (daily/weekly)</p>
                                    <p>5. Ensure the data format matches the expected XML structure</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Import XML File Card */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Import .xml file</CardTitle>
                            <CardDescription>
                                Upload an XML file containing your health data to import it into the system.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <label htmlFor="file-input" className="text-sm font-medium">
                                    Select XML file
                                </label>
                                <Input
                                    id="file-input"
                                    type="file"
                                    accept=".xml"
                                    onChange={handleFileSelect}
                                    ref={fileInputRef}
                                    disabled={loading}
                                />
                                {selectedFile && (
                                    <p className="text-sm text-muted-foreground">
                                        Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)
                                    </p>
                                )}
                            </div>

                            {error && (
                                <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                                    Error: {error}
                                </div>
                            )}

                            {success && (
                                <div className="p-3 text-sm text-green-600 bg-green-50 border border-green-200 rounded-md">
                                    Data imported successfully!
                                </div>
                            )}

                            <div className="flex gap-2">
                                <Button
                                    onClick={handleImport}
                                    disabled={!selectedFile || loading}
                                >
                                    {loading ? 'Importing...' : 'Import Data'}
                                </Button>

                                {selectedFile && (
                                    <Button
                                        variant="outline"
                                        onClick={() => {
                                            setSelectedFile(null);
                                            if (fileInputRef.current) {
                                                fileInputRef.current.value = '';
                                            }
                                            reset();
                                        }}
                                        disabled={loading}
                                    >
                                        Clear
                                    </Button>
                                )}
                            </div>

                            <div className="text-sm text-muted-foreground">
                                <p><strong>Supported format:</strong> XML file</p>
                                <p><strong>File size limit:</strong> 10MB</p>
                                <p><strong>Note:</strong> The file should contain valid health data in the expected format.</p>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="mcp" className="space-y-6">
                    {/* MCP Server Configuration Card */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Configuration for MCP server</CardTitle>
                            <CardDescription>
                                Configure your MCP server to connect with Healthion.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <p className="text-sm font-medium">MCP API Key:</p>
                                <div className="flex gap-2">
                                    <Button
                                        onClick={handleGenerateToken}
                                        variant="outline"
                                    >
                                        Generate Token
                                    </Button>
                                    {showToken && authToken && (
                                        <>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => copyToClipboard(authToken)}
                                            >
                                                Copy Token
                                            </Button>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => setShowToken(false)}
                                            >
                                                Hide
                                            </Button>
                                        </>
                                    )}
                                </div>
                                {showToken && authToken && (
                                    <div className="p-2 bg-muted rounded text-xs font-mono break-all">
                                        {authToken}
                                    </div>
                                )}
                            </div>

                            <div className="space-y-2">
                                <p className="text-sm font-medium">MCP Configuration:</p>
                                <div className="p-4 bg-muted rounded text-sm font-mono overflow-x-auto">
                                    <pre>{JSON.stringify({
                                        "mcpServers": {
                                            "healthion": {
                                                "command": "uvicorn",
                                                "args": ["app.main:app", "--host", "0.0.0.0", "--port", "8000"],
                                                "env": {
                                                    "API_KEY": authToken || "..."
                                                }
                                            }
                                        }
                                    }, null, 2)}</pre>
                                </div>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => copyToClipboard(JSON.stringify({
                                        "mcpServers": {
                                            "healthion": {
                                                "command": "uvicorn",
                                                "args": ["app.main:app", "--host", "0.0.0.0", "--port", "8000"],
                                                "env": {
                                                    "API_KEY": authToken || "..."
                                                }
                                            }
                                        }
                                    }, null, 2))}
                                >
                                    Copy Config
                                </Button>
                            </div>

                            <div className="space-y-2">
                                <p className="text-sm font-medium">How it works:</p>
                                <div className="text-sm text-muted-foreground space-y-1">
                                    <p>• MCP (Model Context Protocol) allows AI assistants to access external tools and data sources</p>
                                    <p>• This configuration connects your MCP server to the Healthion API</p>
                                    <p>• Update the DATABASE_URL with your actual database connection string</p>
                                    <p>• The server will run on port 8000 and provide health data access to MCP clients</p>
                                    <p>• Ensure all required environment variables are set before starting the server</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </>
    );
}
