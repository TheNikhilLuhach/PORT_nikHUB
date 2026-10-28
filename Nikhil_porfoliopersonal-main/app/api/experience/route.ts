import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');
    
    const dataPath = path.join(process.cwd(), 'data', 'experience.json');
    
    if (!fs.existsSync(dataPath)) {
      return NextResponse.json(
        { error: 'Experience data not found' },
        { status: 500 }
      );
    }
    
    const experience = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
    
    if (id) {
      const exp = experience.find((e: { id: number }) => e.id === parseInt(id));
      if (!exp) {
        return NextResponse.json({ error: 'Experience not found' }, { status: 404 });
      }
      return NextResponse.json(exp);
    }
    
    return NextResponse.json(experience);
  } catch (error) {
    console.error('Experience API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
