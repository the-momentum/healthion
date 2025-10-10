import { Routes, Route } from 'react-router-dom'
import { AppLayout } from './components/app-layout'
import { AuthGuard } from './components/auth-guard'
import NotMatch from './pages/NotMatch'
import Dashboard from './pages/Dashboard'
import Sample from './pages/Sample'
import ComingSoon from './pages/ComingSoon'
import Profile from './pages/Profile'

export default function Router() {
    return (
        <Routes>
            <Route element={<AppLayout />}>
                <Route path="" element={
                    <AuthGuard>
                        <Dashboard />
                    </AuthGuard>
                } />
                <Route path="pages">
                    <Route path="sample" element={
                        <AuthGuard>
                            <Sample />
                        </AuthGuard>
                    } />
                    <Route path="profile" element={
                        <AuthGuard>
                            <Profile />
                        </AuthGuard>
                    } />
                    <Route path="feature" element={<ComingSoon />} />
                </Route>
                <Route path="*" element={<NotMatch />} />
            </Route>
        </Routes>
    )
}
