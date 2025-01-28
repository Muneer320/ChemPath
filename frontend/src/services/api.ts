import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  timeout: 10000,
});

export interface Compound {
  id: string;
  name: string;
  formula: string;
  class?: string;
  molecular_weight?: number;
  state?: string;
  aliases?: string[];
  properties?: {
    name?: string;
    molecular_weight?: number;
    state?: string;
    class?: string;
  };
}
export type CompoundResponse = Compound;

export interface ReactionCondition {
  reagent: string;
  temperature?: string;
  pressure?: string;
  mechanism?: string;
  description?: string;
}

export interface PathInfo {
  compounds: Compound[];
  reactions: ReactionCondition[];
  reagents: string[];
  total_steps: number;
  teaching_cost: number;
}

const normalizeCompound = (compound: Compound): Compound => ({
  ...compound,
  properties: {
    name: compound.name,
    molecular_weight: compound.molecular_weight,
    state: compound.state,
    class: compound.class,
  },
});

export const apiService = {
  healthCheck: async () => (await api.get("/health")).data,
  getCompounds: async (search?: string) => {
    const response = await api.get<Compound[]>("/compounds/", { params: search ? { search } : {} });
    return response.data.map(normalizeCompound);
  },
  getCompound: async (identifier: string) => {
    const response = await api.get<Compound>(`/compounds/${encodeURIComponent(identifier)}`);
    return normalizeCompound(response.data);
  },
  getCompoundSuggestions: async (prefix: string, limit = 10) => {
    const response = await api.get<Compound[]>("/compounds/suggestions/", { params: { prefix, limit } });
    return response.data.map(normalizeCompound);
  },
  findPaths: async (start: string, end: string, maxSteps = 5): Promise<PathInfo[]> => {
    const response = await api.get<PathInfo[]>("/paths/", { params: { start, end, max_steps: maxSteps } });
    return response.data.map((path) => ({ ...path, compounds: path.compounds.map(normalizeCompound) }));
  },
};

export default apiService;
