/**
 * Project Store (Zustand)
 * POC Version - Simple state management
 */

import { create } from 'zustand';
import { projectsApi } from '../services/api';

interface Project {
  id: string;
  name: string;
  api_key: string;
  domain?: string; // Pinterest DS: Product Surface / Environment (e.g., Home Feed, Search, Boards)
  created_at: string;
  updated_at: string;
}

interface ProjectStore {
  projects: Project[];
  currentProject: Project | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  fetchProjects: () => Promise<void>;
  setCurrentProject: (project: Project | null) => void;
  createProject: (name: string, domain?: string) => Promise<Project | null>;
  clearError: () => void;
}

export const useProjectStore = create<ProjectStore>((set, get) => ({
  projects: [],
  currentProject: null,
  loading: false,
  error: null,

  fetchProjects: async () => {
    set({ loading: true, error: null });
    try {
      const response = await projectsApi.list();
      const projects = response.data;
      set({ projects, loading: false });
      
      // Auto-select first project if none selected
      if (projects.length > 0 && !get().currentProject) {
        set({ currentProject: projects[0] });
      }
    } catch (error: any) {
      console.error('Failed to fetch projects:', error);
      console.error('Error details:', {
        message: error.message,
        response: error.response,
        request: error.request,
        config: error.config,
      });
      let errorMessage = 'Failed to fetch projects';
      if (error.response) {
        // Server responded with error
        errorMessage = error.response.data?.detail || error.response.data?.message || `Server error: ${error.response.status}`;
        console.error('Response error:', error.response.status, error.response.data);
      } else if (error.request) {
        // Request made but no response (backend not running, CORS issue, or network error)
        console.error('No response received. Request details:', error.request);
        if (error.message && error.message.includes('CORS')) {
          errorMessage = 'CORS error: Backend is running but CORS is blocking the request. Check CORS configuration.';
        } else if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
          errorMessage = `Network error: Cannot connect to backend at ${error.config?.baseURL || 'http://localhost:8000/api/v1'}. Make sure the backend server is running.`;
        } else {
          errorMessage = `Cannot connect to backend. Error: ${error.message || 'Network error'}. Check if backend is running on http://localhost:8000`;
        }
      } else {
        // Something else happened
        errorMessage = `Error: ${error.message || 'Unknown error'}`;
      }
      set({ 
        error: errorMessage,
        loading: false 
      });
    }
  },

  setCurrentProject: (project) => {
    set({ currentProject: project });
  },

  createProject: async (name: string, domain?: string) => {
    set({ loading: true, error: null });
    try {
      const response = await projectsApi.create({ name, domain });
      const newProject = response.data;
      set((state) => ({
        projects: [...state.projects, newProject],
        currentProject: newProject,
        loading: false,
      }));
      return newProject;
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to create project',
        loading: false 
      });
      return null;
    }
  },

  clearError: () => {
    set({ error: null });
  },
}));
