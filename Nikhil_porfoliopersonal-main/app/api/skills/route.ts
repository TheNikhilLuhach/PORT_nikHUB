import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs';

export async function GET() {
  try {
    const dataPath = path.join(process.cwd(), 'data', 'skills.json');
    
    if (!fs.existsSync(dataPath)) {
      return NextResponse.json(
        { error: 'Skills data not found' },
        { status: 500 }
      );
    }
    
    const skills = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
    return NextResponse.json(skills);
  } catch (error) {
    console.error('Skills API Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
