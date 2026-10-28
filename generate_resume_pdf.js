const fs = require('fs');
const path = require('path');

class PDFDocumentWriter {
  constructor() {
    this.objects = [];
    this.streams = [];
    this.fonts = [
      { id: 4, name: 'F1', base: 'Helvetica' },
      { id: 5, name: 'F2', base: 'Helvetica-Bold' },
      { id: 6, name: 'F3', base: 'Helvetica-Oblique' },
    ];
    this.links = [];
    this.pageWidth = 612; // letter width (points)
    this.pageHeight = 792; // letter height (points)
    this.margin = 36; // 0.5 inch margins
    this.cursorY = this.pageHeight - this.margin;
    this.content = [];
  }

  addObject(content) {
    const objNum = this.objects.length + 1;
    this.objects.push({ num: objNum, content });
    return objNum;
  }

  escapeText(text) {
    return text.replace(/\\/g, '\\\\').replace(/\(/g, '\\(').replace(/\)/g, '\\)');
  }

  addText(text, x, y, options = {}) {
    const font = options.font || 'F1';
    const size = options.size || 10;
    const color = options.color || [0, 0, 0];
    
    this.content.push('BT');
    this.content.push(`/${font} ${size} Tf`);
    this.content.push(`${color[0]} ${color[1]} ${color[2]} rg`);
    this.content.push(`1 0 0 1 ${x.toFixed(2)} ${y.toFixed(2)} Tm`);
    this.content.push(`(${this.escapeText(text)}) Tj`);
    this.content.push('ET');
  }

  addCenteredText(text, y, options = {}) {
    const font = options.font || 'F1';
    const size = options.size || 10;
    // Approximate Helvetica character width calculation
    const avgCharWidth = (font === 'F2' ? 0.55 : 0.5) * size;
    const textWidth = text.length * avgCharWidth;
    const x = Math.max(this.margin, (this.pageWidth - textWidth) / 2);
    this.addText(text, x, y, options);
    return x;
  }

  addLine(x1, y1, x2, y2, color = [0.2, 0.2, 0.2], width = 0.75) {
    this.content.push(`${width} w`);
    this.content.push(`${color[0]} ${color[1]} ${color[2]} RG`);
    this.content.push(`${x1.toFixed(2)} ${y1.toFixed(2)} m`);
    this.content.push(`${x2.toFixed(2)} ${y2.toFixed(2)} l`);
    this.content.push('S');
  }

  addSection(title) {
    this.cursorY -= 14;
    this.addText(title.toUpperCase(), this.margin, this.cursorY, { font: 'F2', size: 10.5, color: [0.05, 0.1, 0.2] });
    this.cursorY -= 3;
    this.addLine(this.margin, this.cursorY, this.pageWidth - this.margin, this.cursorY, [0.3, 0.3, 0.3], 0.75);
    this.cursorY -= 10;
  }

  addBulletItem(title, text) {
    const bulletX = this.margin + 8;
    const textX = this.margin + 18;
    this.addText('•', bulletX, this.cursorY, { font: 'F1', size: 9, color: [0.1, 0.1, 0.1] });
    
    if (title) {
      this.addText(title, textX, this.cursorY, { font: 'F2', size: 9, color: [0.1, 0.1, 0.1] });
      const titleWidth = title.length * 4.8;
      this.addText(text, textX + titleWidth, this.cursorY, { font: 'F1', size: 9, color: [0.2, 0.2, 0.2] });
    } else {
      this.addText(text, textX, this.cursorY, { font: 'F1', size: 9, color: [0.2, 0.2, 0.2] });
    }
    this.cursorY -= 11.5;
  }

  addJobHeading(role, duration, company, location) {
    this.addText(role, this.margin, this.cursorY, { font: 'F2', size: 9.5, color: [0.05, 0.1, 0.15] });
    const durationX = this.pageWidth - this.margin - (duration.length * 5.2);
    this.addText(duration, durationX, this.cursorY, { font: 'F2', size: 9, color: [0.1, 0.1, 0.1] });
    this.cursorY -= 10;
    
    this.addText(company, this.margin, this.cursorY, { font: 'F3', size: 9, color: [0.2, 0.2, 0.2] });
    const locationX = this.pageWidth - this.margin - (location.length * 4.8);
    this.addText(location, locationX, this.cursorY, { font: 'F3', size: 8.5, color: [0.3, 0.3, 0.3] });
    this.cursorY -= 10.5;
  }

  addProjectHeading(name, techStack) {
    this.addText(name, this.margin, this.cursorY, { font: 'F2', size: 9.5, color: [0.05, 0.1, 0.2] });
    const nameWidth = name.length * 5.5;
    this.addText(` | ${techStack}`, this.margin + nameWidth, this.cursorY, { font: 'F3', size: 8.5, color: [0.3, 0.3, 0.3] });
    this.cursorY -= 10.5;
  }

  buildPDF() {
    // 1: Catalog
    // 2: Pages
    // 3: Page 1
    // 4, 5, 6: Fonts
    // 7: Content stream
    const contentStream = this.content.join('\n');
    const streamLen = Buffer.byteLength(contentStream, 'utf8');

    const obj3_page = `<<
  /Type /Page
  /Parent 2 0 R
  /MediaBox [0 0 ${this.pageWidth} ${this.pageHeight}]
  /Contents 7 0 R
  /Resources <<
    /Font <<
      /F1 4 0 R
      /F2 5 0 R
      /F3 6 0 R
    >>
  >>
>>`;

    const obj4_font = `<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>`;
    const obj5_font = `<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>`;
    const obj6_font = `<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>`;

    const obj7_stream = `<< /Length ${streamLen} >>\nstream\n${contentStream}\nendstream`;

    const obj2_pages = `<< /Type /Pages /Kids [3 0 R] /Count 1 >>`;
    const obj1_catalog = `<< /Type /Catalog /Pages 2 0 R >>`;

    const allObjects = [
      obj1_catalog,
      obj2_pages,
      obj3_page,
      obj4_font,
      obj5_font,
      obj6_font,
      obj7_stream
    ];

    let output = '%PDF-1.4\n%âãÏÓ\n';
    const offsets = [];

    for (let i = 0; i < allObjects.length; i++) {
      offsets.push(output.length);
      output += `${i + 1} 0 obj\n${allObjects[i]}\nendobj\n`;
    }

    const startXref = output.length;
    output += `xref\n0 ${allObjects.length + 1}\n0000000000 65535 f \n`;
    for (let i = 0; i < offsets.length; i++) {
      output += `${offsets[i].toString().padStart(10, '0')} 00000 n \n`;
    }

    output += `trailer\n<< /Size ${allObjects.length + 1} /Root 1 0 R >>\nstartxref\n${startXref}\n%%EOF\n`;
    return Buffer.from(output, 'binary');
  }
}

function generateResume() {
  const doc = new PDFDocumentWriter();

  // Name & Header
  doc.addCenteredText('NIKHIL KUMAR', doc.cursorY, { font: 'F2', size: 18, color: [0.08, 0.12, 0.25] });
  doc.cursorY -= 13;
  doc.addCenteredText('Software Engineer | Python Developer | Cloud & Automation Specialist', doc.cursorY, { font: 'F2', size: 10, color: [0.15, 0.2, 0.35] });
  doc.cursorY -= 12;

  const contactText = 'nikuluhach.86209@gmail.com | +91 7297072067 | Jaipur, Rajasthan, India';
  doc.addCenteredText(contactText, doc.cursorY, { font: 'F1', size: 8.5, color: [0.25, 0.25, 0.25] });
  doc.cursorY -= 10;
  
  const linksText = 'LinkedIn: nikhil-kumar-692116203 | GitHub: TheNikhilLuhach | Portfolio: porfolio-six-smoky-21.vercel.app';
  doc.addCenteredText(linksText, doc.cursorY, { font: 'F1', size: 8.5, color: [0.1, 0.3, 0.6] });
  doc.cursorY -= 6;

  // Education
  doc.addSection('Education');
  doc.addJobHeading('Bachelor of Technology in Computer Science and Engineering', '2023 – 2027', 'Amity University Rajasthan', 'Jaipur, India');
  doc.addBulletItem('', 'Core coursework: Data Structures, Algorithms, OOP, Database Management Systems, Operating Systems, Computer Networks.');
  doc.cursorY -= 2;

  // Technical Skills
  doc.addSection('Technical Skills');
  doc.addBulletItem('Programming Languages: ', 'Python, Java, C, C++, JavaScript, TypeScript, Bash/Shell Scripting');
  doc.addBulletItem('Web & Frameworks: ', 'Next.js, React, Node.js, Flask, FastAPI, REST APIs, HTML5, CSS3, Tailwind CSS');
  doc.addBulletItem('Cloud & DevOps: ', 'AWS (EC2, S3, IAM, CLI), Docker, Linux Server Administration, Git, GitHub, CI/CD');
  doc.addBulletItem('AI & Automation: ', 'Generative AI, Google Gemini API, Prompt Engineering, PyAutoGUI, MediaPipe, OpenCV');
  doc.addBulletItem('Databases & Tools: ', 'MySQL, MongoDB, SQLite, Postman, VS Code, Kali Linux, Burp Suite');
  doc.cursorY -= 2;

  // Experience
  doc.addSection('Work Experience & Internships');
  
  doc.addJobHeading('DevOps Trainee', 'Jun 2026 – Jul 2026', 'LinuxWorld Informatics Pvt. Ltd.', 'Remote');
  doc.addBulletItem('', 'Configured CI/CD automation pipelines and managed containerized workloads using Docker on Linux.');
  doc.addBulletItem('', 'Administered cloud instances, hardened security permissions, and automated routine deployment tasks.');

  doc.addJobHeading('Python Developer Intern', 'Dec 2025 – Jun 2026', 'The Skybrisk', 'Remote');
  doc.addBulletItem('', 'Engineered Python backend microservices, REST APIs, and automated task-scheduling workflows.');
  doc.addBulletItem('', 'Implemented data processing pipelines, structured exception handling, and backend performance validation.');

  doc.addJobHeading('Generative AI Trainee', 'May 2025 – Aug 2025', 'LinuxWorld Informatics Pvt. Ltd.', 'Remote');
  doc.addBulletItem('', 'Constructed Generative AI solutions and conversational workflows leveraging Google Gemini models.');
  doc.addBulletItem('', 'Developed structured prompt templates and response-parsing pipelines for project recommendation engines.');

  doc.addJobHeading('AWS Cloud Computing Trainee', 'Jun 2024 – Aug 2024', 'LinuxWorld Informatics Pvt. Ltd.', 'Remote');
  doc.addBulletItem('', 'Provisioned and managed AWS infrastructure including Amazon EC2 instances, S3 storage, and IAM policies.');
  doc.addBulletItem('', 'Automated administrative server routines and resource auditing via AWS CLI and Linux Bash scripts.');

  doc.addJobHeading('Web Development Intern', 'Mar 2024 – Apr 2024', '1Stop.ai', 'Remote');
  doc.addBulletItem('', 'Developed responsive web components adhering to modern HTML5, CSS3, and JavaScript best practices.');
  doc.addBulletItem('', 'Enhanced cross-browser rendering fidelity, layout fluidity, and user accessibility.');
  doc.cursorY -= 2;

  // Projects
  doc.addSection('Key Projects');
  
  doc.addProjectHeading('Tech2Idea AI Chatbot', 'Python, Streamlit, Google Gemini API, NLP, Prompt Engineering');
  doc.addBulletItem('', 'Conversational AI converting technical proficiencies into structured, actionable project specifications.');
  doc.addBulletItem('', 'Implemented multi-turn dialogue, real-time Gemini generation, and user-provided API key security.');

  doc.addProjectHeading('CareerPilot Platform', 'Python, Flask, SQLAlchemy, Tailwind CSS, SQLite, CSRF Protection');
  doc.addBulletItem('', 'Full-stack career development portal with user authentication, job matching, and technical assessments.');
  doc.addBulletItem('', 'Engineered algorithmic ATS resume scorer evaluating keyword density, formatting, and completeness.');

  doc.addProjectHeading('Hand Gesture Control System', 'Python, OpenCV, MediaPipe, PyAutoGUI');
  doc.addBulletItem('', 'Computer vision application enabling touchless OS control via webcam hand tracking & landmark detection.');
  doc.addBulletItem('', 'Engineered gesture classification with debounce cooldown timers to prevent spurious command triggers.');

  doc.addProjectHeading('StudySync Learning Hub', 'Flask-SocketIO, WebRTC, HTML5 Canvas, OpenAI API');
  doc.addBulletItem('', 'Real-time collaborative study platform featuring interactive canvas whiteboard and AI tutoring assistant.');

  doc.addProjectHeading('Voice-Controlled Automation Menu', 'Python, SpeechRecognition, PyAutoGUI, Windows Automation');
  doc.addBulletItem('', 'Desktop voice assistant automating application launching, file explorer actions, and window management.');
  doc.cursorY -= 2;

  // Achievements & Certifications
  doc.addSection('Achievements & Certifications');
  doc.addBulletItem('Hackathon Award: ', 'Second Position in college-level hackathon with the Nexora project.');
  doc.addBulletItem('Athletic Achievement: ', 'District-level Silver Medal in Karate.');
  doc.addBulletItem('Certifications: ', 'Generative AI (LinuxWorld) | AWS Cloud Computing (LinuxWorld) | Python Dev (The Skybrisk) | DevOps (LinuxWorld) | Web Dev (1Stop.ai)');

  const pdfBuffer = doc.buildPDF();
  const outputPath = path.join(__dirname, 'porfolio', 'public', 'resume', 'Nikhil_Kumar_Resume.pdf');
  fs.writeFileSync(outputPath, pdfBuffer);
  console.log(`Generated resume PDF: ${outputPath} (${pdfBuffer.length} bytes)`);
}

generateResume();
