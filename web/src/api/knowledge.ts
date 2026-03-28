import axios from 'axios';

const API_BASE = '/api';

export interface KnowledgeUnit {
  id: string;
  title: string;
  problem: string;
  solution: string;
  context: Record<string, unknown>;
  confidence: number;
  usage_count: number;
  created_at: string;
  updated_at: string;
  source: string;
  verified: boolean;
  tags: string[];
}

export interface KnowledgeCreate {
  title: string;
  problem: string;
  solution: string;
  tags?: string[];
  confidence?: number;
  source?: string;
}

export interface FeedbackStats {
  helpful_count: number;
  not_helpful_count: number;
  total_count: number;
}

export const knowledgeApi = {
  /** List knowledge units with optional search and filtering */
  list: async (params: {
    search?: string;
    tags?: string;
    limit?: number;
    offset?: number;
  } = {}) => {
    const response = await axios.get<KnowledgeUnit[]>(`${API_BASE}/knowledge`, {
      params,
    });
    return response.data;
  },

  /** Get a single knowledge unit by ID */
  get: async (id: string) => {
    const response = await axios.get<KnowledgeUnit>(`${API_BASE}/knowledge/${id}`);
    return response.data;
  },

  /** Create a new knowledge unit */
  create: async (data: KnowledgeCreate) => {
    const response = await axios.post<KnowledgeUnit>(`${API_BASE}/knowledge`, data);
    return response.data;
  },

  /** Delete a knowledge unit */
  delete: async (id: string) => {
    await axios.delete(`${API_BASE}/knowledge/${id}`);
  },

  /** Add feedback for a knowledge unit */
  addFeedback: async (id: string, helpful: boolean, source?: string) => {
    const response = await axios.post<FeedbackStats>(
      `${API_BASE}/knowledge/${id}/feedback`,
      { helpful, source },
    );
    return response.data;
  },

  /** Get feedback statistics for a knowledge unit */
  getFeedbackStats: async (id: string) => {
    const response = await axios.get<FeedbackStats>(
      `${API_BASE}/knowledge/${id}/feedback`,
    );
    return response.data;
  },
};
