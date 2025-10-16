import { Routes, Route } from 'react-router-dom'
import { AppLayout } from './components/app-layout'
import { AuthGuard } from './components/auth-guard'
import NotMatch from './pages/NotMatch'
import Dashboard from './pages/Dashboard'
import Sample from './pages/Sample'
import ComingSoon from './pages/ComingSoon'
import Profile from './pages/Profile'
import ImportData from './pages/ImportData'
import HeartRate from './pages/HeartRate'
import Workouts from './pages/Workouts'

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
                    <Route path="import" element={
                        <AuthGuard>
                            <ImportData />
                        </AuthGuard>
                    } />
                    <Route path="heart-rate" element={
                        <AuthGuard>
                            <HeartRate />
                        </AuthGuard>
                    } />
                    <Route path="workouts" element={
                        <AuthGuard>
                            <Workouts />
                        </AuthGuard>
                    } />
                    <Route path="feature" element={<ComingSoon />} />
                </Route>
                <Route path="*" element={<NotMatch />} />
            </Route>
        </Routes>
    )
}
