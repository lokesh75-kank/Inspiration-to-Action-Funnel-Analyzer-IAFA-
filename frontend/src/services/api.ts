/**
 * API Client for IAFA Backend
 * POC Version - No authentication required
 */

import axios from 'axios';

// Use Vite proxy for development, or full URL for production
const API_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '/api/v1' : 'http://localhost:8000/api/v1');

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (for future auth if needed)
apiClient.interceptors.request.use(
  (config) => {
    // POC: No auth token needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// API Methods

// Projects
export const projectsApi = {
  list: () => apiClient.get('/projects'),
  get: (id: string) => apiClient.get(`/projects/${id}`),
  create: (data: { name: string; domain?: string }) => 
    apiClient.post('/projects', data),
  update: (id: string, data: { name: string; domain?: string }) =>
    apiClient.put(`/projects/${id}`, data),
  delete: (id: string) => apiClient.delete(`/projects/${id}`),
  getTrackingCode: (id: string) => apiClient.get(`/projects/${id}/tracking-code`),
};

// Funnels
export const funnelsApi = {
  list: (projectId?: string) => {
    const params = projectId ? { project_id: projectId } : {};
    return apiClient.get('/funnels', { params });
  },
  get: (id: string) => apiClient.get(`/funnels/${id}`),
  create: (data: {
    project_id: string;
    name: string;
    description?: string;
    stages: Array<{ order: number; name: string; event_type: string }>;
  }) => apiClient.post('/funnels', data),
  update: (id: string, data: {
    project_id: string;
    name: string;
    description?: string;
    stages: Array<{ order: number; name: string; event_type: string }>;
  }) => apiClient.put(`/funnels/${id}`, data),
  delete: (id: string) => apiClient.delete(`/funnels/${id}`),
};

// Events
export const eventsApi = {
  getEventTypes: (projectId: string) => 
    apiClient.get<string[]>('/events/types', { 
      params: { project_id: projectId } 
    }),
}

// Analytics
export const analyticsApi = {
  getFunnelAnalytics: (
    funnelId: string, 
    startDate: string, 
    endDate: string,
    filters?: {
      user_intent?: string[];
      content_category?: string[];
      surface?: string[];
      user_tenure?: string[];
      segment_by?: string;
    }
  ) => {
    const params: any = { start_date: startDate, end_date: endDate };
    
    // Add segment filters
    if (filters?.user_intent && filters.user_intent.length > 0) {
      params.user_intent = filters.user_intent.join(',');
    }
    if (filters?.content_category && filters.content_category.length > 0) {
      params.content_category = filters.content_category.join(',');
    }
    if (filters?.surface && filters.surface.length > 0) {
      params.surface = filters.surface.join(',');
    }
    if (filters?.user_tenure && filters.user_tenure.length > 0) {
      params.user_tenure = filters.user_tenure.join(',');
    }
    if (filters?.segment_by) {
      params.segment_by = filters.segment_by;
    }
    
    return apiClient.get(`/analytics/funnel/${funnelId}`, { params });
  },
  getFunnelRecommendations: (
    funnelId: string,
    startDate: string,
    endDate: string,
    filters?: {
      user_intent?: string[];
      content_category?: string[];
      surface?: string[];
      user_tenure?: string[];
      segment_by?: string;
    },
    orgId: string = 'poc-org',
    audience: string = 'data_scientist'
  ) => {
    const segment_filters: any = {};
    if (filters?.user_intent && filters.user_intent.length > 0) {
      segment_filters.user_intent = filters.user_intent;
    }
    if (filters?.content_category && filters.content_category.length > 0) {
      segment_filters.content_category = filters.content_category;
    }
    if (filters?.surface && filters.surface.length > 0) {
      segment_filters.surface = filters.surface;
    }
    if (filters?.user_tenure && filters.user_tenure.length > 0) {
      segment_filters.user_tenure = filters.user_tenure;
    }
    
    return apiClient.post(`/analytics/funnel/${funnelId}/recommendations`, {
      org_id: orgId,
      start_date: startDate,
      end_date: endDate,
      segment_filters,
      segment_by: filters?.segment_by,
      audience
    });
  },
  generateAIReport: (
    funnelId: string,
    startDate: string,
    endDate: string,
    filters?: {
      user_intent?: string[];
      content_category?: string[];
      surface?: string[];
      user_tenure?: string[];
      segment_by?: string;
    },
    orgId: string = 'poc-org',
    audience: string = 'data_scientist',
    format: string = 'html'
  ) => {
    const segment_filters: any = {};
    if (filters?.user_intent && filters.user_intent.length > 0) {
      segment_filters.user_intent = filters.user_intent;
    }
    if (filters?.content_category && filters.content_category.length > 0) {
      segment_filters.content_category = filters.content_category;
    }
    if (filters?.surface && filters.surface.length > 0) {
      segment_filters.surface = filters.surface;
    }
    if (filters?.user_tenure && filters.user_tenure.length > 0) {
      segment_filters.user_tenure = filters.user_tenure;
    }
    
    return apiClient.post(`/analytics/funnel/${funnelId}/report`, {
      org_id: orgId,
      start_date: startDate,
      end_date: endDate,
      segment_filters,
      segment_by: filters?.segment_by,
      audience,
      format
    });
  },
};

// Tracking (for external use)
export const trackingApi = {
  track: (apiKey: string, event: {
    event_type: string;
    user_id: string;
    session_id?: string;
    properties?: Record<string, any>;
    url?: string;
    referrer?: string;
    user_agent?: string;
    timestamp?: string;
  }) =>
    apiClient.post('/track', event, {
      headers: { 'X-API-Key': apiKey },
    }),
  trackBatch: (apiKey: string, events: Array<any>) =>
    apiClient.post('/track/batch', { events }, {
      headers: { 'X-API-Key': apiKey },
    }),
};

export default apiClient;
