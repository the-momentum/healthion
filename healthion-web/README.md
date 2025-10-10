# React Shadcn Starter

React + Vite + TypeScript template for building apps with shadcn/ui.

## Getting Started

```bash
npx degit hayyi2/react-shadcn-starter my-project
cd my-project
npm install
npm run dev
```

## Authentication with Auth0

This starter includes Auth0 integration for secure authentication. To set it up:

### 1. Create an Auth0 Application

1. Go to [Auth0 Dashboard](https://manage.auth0.com/)
2. Create a new **Single Page Application**
3. Configure the following settings:
   - **Allowed Callback URLs**: `http://localhost:3000`
   - **Allowed Logout URLs**: `http://localhost:3000`
   - **Allowed Web Origins**: `http://localhost:3000`

### 2. Configure Environment Variables

Update the `.env` file with your Auth0 credentials:

```env
# Auth0 Configuration
VITE_AUTH0_DOMAIN=your-auth0-domain.auth0.com
VITE_AUTH0_CLIENT_ID=your-auth0-client-id
VITE_AUTH0_AUDIENCE=https://your-auth0-domain.auth0.com/api/v2/
```

Replace the placeholder values with your actual Auth0 application settings.

### 3. Features Included

- 🔐 **Secure Authentication**: Login/logout with Auth0
- 🛡️ **Protected Routes**: Dashboard and Sample pages require authentication
- 👤 **User Profile**: View user information and manage account
- 🎨 **UI Integration**: Seamless integration with shadcn/ui components

### 4. Usage

```tsx
import { useAuth } from '@/hooks/use-auth'

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth()

  if (!isAuthenticated) {
    return <button onClick={login}>Sign In</button>
  }

  return (
    <div>
      <p>Welcome, {user?.name}!</p>
      <button onClick={logout}>Sign Out</button>
    </div>
  )
}
```

## Getting Done

- [x] Single page app with navigation and responsif layout
- [x] Customable configuration `/config`
- [x] Simple starting page/feature `/pages`
- [x] Github action deploy github pages
- [x] Auth0 authentication integration

## Deploy `gh-pages`

- change `basenameProd` in `/vite.config.ts`
- create deploy key `GITHUB_TOKEN` in github `/settings/keys`
- commit and push changes code
- setup gihub pages to branch `gh-pages`
- run action `Build & Deploy`

### Auto Deploy

- change file `.github/workflows/build-and-deploy.yml`
- Comment on `workflow_dispatch`
- Uncomment on `push`

```yaml
# on:
#   workflow_dispatch:
on:
  push:
    branches: ["main"]
```

## Features

- React + Vite + TypeScript
- Tailwind CSS
- [shadcn-ui](https://github.com/shadcn-ui/ui/)
- [react-router-dom](https://www.npmjs.com/package/react-router-dom)
- [Auth0](https://auth0.com/) authentication

## Project Structure

```md
react-shadcn-starter/
├── public/            # Public assets
├── src/               # Application source code
│   ├── components/    # React components
│   ├── context/       # contexts components
│   ├── config/        # Config data
│   ├── hook/          # Custom hooks
│   ├── lib/           # Utility functions
│   ├── pages/         # pages/features components
│   ├── App.tsx        # Application entry point
│   ├── index.css      # Main css and tailwind configuration
│   ├── main.tsx       # Main rendering file
│   └── Router.tsx     # Routes component
├── index.html         # HTML entry point
├── tsconfig.json      # TypeScript configuration
└── vite.config.ts     # Vite configuration
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/hayyi2/react-shadcn-starter/blob/main/LICENSE) file for details.
