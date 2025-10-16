import {
    Gauge,
    Upload,
    Heart,
    Activity,
    LucideIcon
} from 'lucide-react'

type MenuItemType = {
    title: string
    url: string
    external?: string
    icon?: LucideIcon
    items?: MenuItemType[]
}
type MenuType = MenuItemType[]

export const mainMenu: MenuType = [
    {
        title: 'Dashboard',
        url: '/',
        icon: Gauge
    },
    {
        title: 'Heart Rate',
        url: '/pages/heart-rate',
        icon: Heart
    },
    {
        title: 'Workouts',
        url: '/pages/workouts',
        icon: Activity
    },
    {
        title: 'Connect Data',
        url: '/pages/import',
        icon: Upload
    },
]
