export interface Project {
  id: number;
  name: string;
  folder: string;
  description: string;
  tech: string[];
  features?: string[];
  liveLink: string;
  githubLink: string;
}

// Use empty string for same-origin (Vercel/Next.js API routes), or set NEXT_PUBLIC_API_URL for external backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? '';

export async function getProjects(): Promise<Project[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/projects`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Failed to fetch projects');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching projects:', error);
    throw error;
  }
}

export async function getSkills() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/skills`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Failed to fetch skills');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching skills:', error);
    throw error;
  }
}

export async function getExperience() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/experience`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Failed to fetch experience');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching experience:', error);
    throw error;
  }
}
