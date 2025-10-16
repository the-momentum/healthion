type AppConfigType = {
    name: string,
    github: {
        title: string,
        url: string
    },
    author: {
        name: string,
        url: string
    },
    auth0: {
        domain: string,
        clientId: string,
        audience: string,
    },
    api: {
        baseUrl: string,
    },
}

export const appConfig: AppConfigType = {
    name: import.meta.env.VITE_APP_NAME ?? "Healthion",
    github: {
        title: "Healthion Web",
        url: "https://github.com/your-username/healthion-web",
    },
    author: {
        name: "Healthion Team",
        url: "https://github.com/your-username/",
    },
    auth0: {
        domain: import.meta.env.VITE_AUTH0_DOMAIN ?? "",
        clientId: import.meta.env.VITE_AUTH0_CLIENT_ID ?? "",
        audience: import.meta.env.VITE_AUTH0_AUDIENCE ?? "healthion-api",
    },
    api: {
        baseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1",
    },
}

export const baseUrl = import.meta.env.VITE_BASE_URL ?? ""
