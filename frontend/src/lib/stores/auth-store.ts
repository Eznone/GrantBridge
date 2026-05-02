'use client'

import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { User } from '@/types/user'

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

// Mock user data
const mockUser: User = {
  id: '1',
  email: 'demo@grantbridge.org',
  name: 'Demo User',
  organizationId: 'org-1',
  role: 'admin',
  createdAt: new Date().toISOString(),
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
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 800))
          
          // Mock validation
          if (email === 'demo@grantbridge.org' && password === 'demo123') {
            const mockToken = 'mock-jwt-token-' + Date.now()
            
            set({
              user: mockUser,
              token: mockToken,
              isAuthenticated: true,
              isLoading: false,
              error: null,
            })
          } else {
            set({
              error: 'Invalid email or password',
              isLoading: false,
              isAuthenticated: false,
            })
            throw new Error('Invalid credentials')
          }
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Login failed',
          })
          throw error
        }
      },

      register: async (name: string, email: string, password: string) => {
        set({ isLoading: true, error: null })
        
        try {
          // Simulate API call
          await new Promise(resolve => setTimeout(resolve, 800))
          
          const newUser: User = {
            ...mockUser,
            id: 'user-' + Date.now(),
            name,
            email,
          }
          
          const mockToken = 'mock-jwt-token-' + Date.now()
          
          set({
            user: newUser,
            token: mockToken,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          })
        } catch (error) {
          set({
            isLoading: false,
            error: error instanceof Error ? error.message : 'Registration failed',
          })
          throw error
        }
      },

      logout: () => {
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
