import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');
    
    const dataPath = path.join(process.cwd(), 'data', 'projects.json');
    
    if (!fs.existsSync(dataPath)) {
      return NextResponse.json(
        { error: 'Projects data not found' },
        { status: 500 }
      );
    }
    
    const projects = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
    
    if (id) {
      const project = projects.find((p: { id: number }) => p.id === parseInt(id));
      if (!project) {
        return NextResponse.json({ error: 'Project not found' }, { status: 404 });
      }
      return NextResponse.json(project);
    }
    
    return NextResponse.json(projects);
  } catch (error) {
    console.error('Projects API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
