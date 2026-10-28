'use client';

import { motion, useInView, AnimatePresence } from 'framer-motion';
import { useRef, useEffect, useState } from 'react';
import { 
  ExternalLink, 
  Github, 
  Layers, 
  Loader2,
  Folder,
  Sparkles,
  Play,
  X
} from 'lucide-react';
import { getProjects, Project } from '@/app/services/api';

const techColors: Record<string, string> = {
  Python: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
  JavaScript: 'bg-yellow-400/20 text-yellow-200 border-yellow-400/30',
  React: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
  'Next.js': 'bg-gray-500/20 text-gray-300 border-gray-500/30',
  Node: 'bg-green-500/20 text-green-300 border-green-500/30',
  Express: 'bg-gray-400/20 text-gray-300 border-gray-400/30',
  MongoDB: 'bg-green-600/20 text-green-400 border-green-600/30',
  MySQL: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
  Flask: 'bg-gray-300/20 text-gray-200 border-gray-300/30',
  FastAPI: 'bg-teal-500/20 text-teal-300 border-teal-500/30',
  Docker: 'bg-blue-600/20 text-blue-400 border-blue-600/30',
  AWS: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
  'AWS EC2': 'bg-orange-500/20 text-orange-300 border-orange-500/30',
  Automation: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
  'Machine Learning': 'bg-pink-500/20 text-pink-300 border-pink-500/30',
  AI: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
  'Generative AI tools': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
  Security: 'bg-red-500/20 text-red-300 border-red-500/30',
  'Computer Vision': 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30',
  OpenCV: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30',
  SMTP: 'bg-blue-400/20 text-blue-200 border-blue-400/30',
  'Automation Scripts': 'bg-purple-500/20 text-purple-300 border-purple-500/30',
  'Web Interface': 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
  HTML: 'bg-orange-600/20 text-orange-400 border-orange-600/30',
  CSS: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
  Linux: 'bg-gray-400/20 text-gray-200 border-gray-400/30',
};

function getTechColor(tech: string): string {
  return techColors[tech] || 'bg-accent-cyan/20 text-accent-cyan border-accent-cyan/30';
}

function ProjectCard({ project, index }: { project: Project; index: number }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-50px' });
  const [showPreview, setShowPreview] = useState(false);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ delay: index * 0.1, duration: 0.6 }}
      className="group relative glass rounded-2xl overflow-hidden hover:border-accent-cyan/30 transition-all duration-500"
    >
      {/* Glow Effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent-cyan/10 to-accent-purple/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      
      {/* Preview Modal */}
      <AnimatePresence>
        {showPreview && project.liveLink && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 z-20 flex flex-col bg-dark-900/98 backdrop-blur-sm rounded-2xl"
          >
            <div className="flex items-center justify-between p-4 border-b border-dark-600">
              <span className="text-sm font-medium text-accent-cyan">Project Preview</span>
              <motion.button
                onClick={() => setShowPreview(false)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                className="p-2 rounded-lg hover:bg-dark-700 text-gray-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </motion.button>
            </div>
            <div className="flex-1 min-h-0 p-4">
              <iframe
                src={project.liveLink}
                title={`${project.name} preview`}
                className="w-full h-full min-h-[280px] rounded-xl border border-dark-600 bg-dark-800"
                sandbox="allow-scripts allow-same-origin"
              />
              <a
                href={project.liveLink}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 flex items-center justify-center gap-2 w-full py-2 rounded-lg bg-gradient-to-r from-accent-cyan to-accent-purple text-white text-sm font-medium hover:opacity-90 transition-opacity"
              >
                <ExternalLink className="w-4 h-4" />
                Open Full Demo
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      <div className="relative p-6">
        {/* Icon */}
        <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-accent-cyan/20 to-accent-purple/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
          <Folder className="w-7 h-7 text-accent-cyan" />
        </div>

        {/* Title */}
        <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-accent-cyan transition-colors">
          {project.name}
        </h3>

        {/* Description */}
        <p className="text-gray-400 text-sm mb-4 line-clamp-3 leading-relaxed">
          {project.description}
        </p>

        {/* Features */}
        {project.features && (
          <div className="mb-4">
            <ul className="space-y-1">
              {project.features.slice(0, 3).map((feature: string, idx: number) => (
                <li key={idx} className="flex items-start gap-2 text-gray-400 text-xs">
                  <span className="w-1 h-1 rounded-full bg-accent-cyan mt-1.5 flex-shrink-0" />
                  <span className="line-clamp-1">{feature}</span>
                </li>
              ))}
              {project.features.length > 3 && (
                <li className="text-gray-500 text-xs italic">
                  +{project.features.length - 3} more features
                </li>
              )}
            </ul>
          </div>
        )}

        {/* Tech Stack */}
        <div className="flex flex-wrap gap-2 mb-6">
          {project.tech.slice(0, 4).map((tech) => (
            <span
              key={tech}
              className={`px-2.5 py-1 rounded-full text-xs font-medium border ${getTechColor(tech)}`}
            >
              {tech}
            </span>
          ))}
          {project.tech.length > 4 && (
            <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-dark-600 text-gray-400">
              +{project.tech.length - 4}
            </span>
          )}
        </div>

        {/* Links */}
        <div className="flex flex-wrap gap-2">
          {project.liveLink && (
            <>
              <motion.button
                onClick={() => setShowPreview(true)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-dark-700 hover:bg-accent-cyan/20 border border-accent-cyan/30 text-accent-cyan text-sm font-medium transition-all"
              >
                <Play className="w-3.5 h-3.5" />
                Preview
              </motion.button>
              <motion.a
                href={project.liveLink}
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-gradient-to-r from-accent-cyan to-accent-purple text-white text-sm font-medium hover:shadow-lg hover:shadow-accent-cyan/25 transition-all"
              >
                <ExternalLink className="w-3.5 h-3.5" />
                Live Demo
              </motion.a>
            </>
          )}
          {project.githubLink && (
            <motion.a
              href={project.githubLink}
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-dark-700 hover:bg-dark-600 text-gray-300 hover:text-white transition-all text-sm font-medium"
            >
              <Github className="w-3.5 h-3.5" />
              GitHub
            </motion.a>
          )}
          {!project.liveLink && project.githubLink && (
            <motion.a
              href={project.githubLink}
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-dark-800/50 text-gray-500 text-sm font-medium"
            >
              <Github className="w-3.5 h-3.5" />
              View on GitHub
            </motion.a>
          )}
        </div>
      </div>
    </motion.div>
  );
}

export default function Projects() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAll, setShowAll] = useState(false);
  const displayedProjects = showAll ? projects : projects.slice(0, 4);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const data = await getProjects();
        setProjects(data);
        setError(null);
      } catch (err) {
        setError('Failed to load projects. Please try again later.');
        // Fallback data (with live demo links)
        setProjects([
          {
            id: 1,
            name: 'Hand Gesture Control System',
            folder: 'hand-gesture-control',
            description: 'Computer vision application that enables touchless control using hand gestures and MediaPipe.',
            tech: ['Python', 'Computer Vision', 'AI', 'OpenCV'],
            liveLink: '/projects/hand-gesture-control',
            githubLink: 'https://github.com/TheNikhilLuhach',
          },
          {
            id: 2,
            name: 'Tech2Idea AI Chatbot',
            folder: 'tech2idea-chatbot',
            description: 'AI assistant that transforms technical skills into unique project ideas using Google Gemini.',
            tech: ['Python', 'Streamlit', 'AI', 'NLP'],
            liveLink: '/projects/tech2idea-chatbot',
            githubLink: 'https://github.com/TheNikhilLuhach',
          },
          {
            id: 3,
            name: 'Voice Automation Menu',
            folder: 'voice-automation-menu',
            description: 'Voice-controlled automation system for hands-free computer operation using speech recognition.',
            tech: ['Python', 'AI', 'Automation', 'NLP'],
            liveLink: '/projects/voice-automation-menu',
            githubLink: 'https://github.com/TheNikhilLuhach',
          },
          {
            id: 4,
            name: 'CareerPilot Platform',
            folder: 'careerpilot-platform',
            description: 'AI resume builder with job search, career guidance, and technical assessments.',
            tech: ['Python', 'Flask', 'AI', 'SQLAlchemy'],
            liveLink: '/projects/careerpilot-platform',
            githubLink: 'https://github.com/TheNikhilLuhach',
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  return (
    <section id="projects" className="py-24 relative overflow-hidden">
      {/* Background */}
      <div className="absolute top-0 left-0 w-full h-full grid-overlay opacity-30" />
      <div className="absolute bottom-0 left-1/4 w-96 h-96 bg-accent-purple/10 rounded-full blur-3xl" />

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 40 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          className="max-w-6xl mx-auto"
        >
          {/* Section Header */}
          <div className="text-center mb-16">
            <motion.span
              initial={{ opacity: 0 }}
              animate={isInView ? { opacity: 1 } : {}}
              transition={{ delay: 0.2 }}
              className="inline-block px-4 py-1.5 rounded-full glass text-accent-cyan text-sm font-medium mb-4"
            >
              <Layers className="w-4 h-4 inline mr-2" />
              Featured Work
            </motion.span>
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={isInView ? { opacity: 1, y: 0 } : {}}
              transition={{ delay: 0.3 }}
              className="text-4xl sm:text-5xl font-bold mb-6"
            >
              My <span className="text-gradient">Projects</span>
            </motion.h2>
            <motion.p
              initial={{ opacity: 0 }}
              animate={isInView ? { opacity: 1 } : {}}
              transition={{ delay: 0.4 }}
              className="text-gray-400 max-w-2xl mx-auto"
            >
              A showcase of my best work, featuring automation tools, AI applications,
              and full-stack development projects.
            </motion.p>
          </div>

          {/* Loading State */}
          <AnimatePresence>
            {loading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center justify-center py-20"
              >
                <Loader2 className="w-10 h-10 text-accent-cyan animate-spin mb-4" />
                <p className="text-gray-400">Loading projects...</p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Projects Grid */}
          {!loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="grid grid-cols-1 md:grid-cols-2 gap-6"
            >
              <AnimatePresence>
                {displayedProjects.map((project, index) => (
                  <ProjectCard key={project.id} project={project} index={index} />
                ))}
              </AnimatePresence>
            </motion.div>
          )}

          {/* Show More/Less Button */}
          {!loading && projects.length > 4 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="text-center mt-12"
            >
              <motion.button
                onClick={() => setShowAll(!showAll)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="inline-flex items-center gap-2 px-8 py-4 glass rounded-full text-gray-300 hover:text-white hover:border-accent-cyan/50 transition-all"
              >
                {showAll ? (
                  <>
                    Show Less
                    <span className="text-accent-cyan">▲</span>
                  </>
                ) : (
                  <>
                    Show More
                    <span className="text-accent-cyan">▼</span>
                  </>
                )}
              </motion.button>
            </motion.div>
          )}

          {/* View More on GitHub */}
          {!loading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 }}
              className="text-center mt-6"
            >
              <motion.a
                href="https://github.com/TheNikhilLuhach"
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="inline-flex items-center gap-2 px-8 py-4 glass rounded-full text-gray-300 hover:text-white hover:border-accent-cyan/50 transition-all"
              >
                <Github className="w-5 h-5" />
                View More on GitHub
                <Sparkles className="w-4 h-4 text-accent-cyan" />
              </motion.a>
            </motion.div>
          )}
        </motion.div>
      </div>
    </section>
  );
}
