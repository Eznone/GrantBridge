import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { User } from '@/types/user'
import { authService } from '@/lib/services/auth-service'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  _hasHydrated: boolean
  
  setHasHydrated: (state: boolean) => void
  login: (email: string, password: string) => Promise<void>
  register: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
  clearError: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
      _hasHydrated: false,

      setHasHydrated: (state) => {
        set({ _hasHydrated: state })
      },

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null })
        
        try {
          const response = await authService.login({ email, password })
          
          // Save tokens for api-client and future refreshes
          localStorage.setItem('auth_token', response.token)
          if (response.refreshToken) {
            localStorage.setItem('refresh_token', response.refreshToken)
          }
          
          set({
            user: response.user,
            token: response.token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          })
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.message || 'Login failed',
            isAuthenticated: false,
          })
          throw error
        }
      },

      register: async (name: string, email: string, password: string) => {
        set({ isLoading: true, error: null })
        
        try {
          const response = await authService.register({ name, email, password })
          
          localStorage.setItem('auth_token', response.token)
          if (response.refreshToken) {
            localStorage.setItem('refresh_token', response.refreshToken)
          }
          
          set({
            user: response.user,
            token: response.token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          })
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.message || 'Registration failed',
            isAuthenticated: false,
          })
          throw error
        }
      },

      logout: () => {
        authService.logout()
        localStorage.removeItem('auth_token')
        localStorage.removeItem('refresh_token')
        
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          error: null,
          isLoading: false,
        })
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'grantbridge-auth',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true)
      },
    }
  )
)

// Made with Bob
