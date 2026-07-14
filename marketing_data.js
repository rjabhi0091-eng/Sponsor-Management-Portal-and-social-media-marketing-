// Simple in-memory/local marketing workflow data (front-end only)
// This will be replaced later by DB-backed endpoints if/when you add them to FastAPI.

export const seedCampaigns = [
  { id: 1, name: 'Sponsor Post Series - Q3', status: 'planned', nextStep: 'Schedule drafts', channel: 'Instagram' },
  { id: 2, name: 'Influencer Outreach', status: 'active', nextStep: 'Collect briefs', channel: 'LinkedIn' },
  { id: 3, name: 'Paid Promotion Sprint', status: 'completed', nextStep: 'Review results', channel: 'Twitter' },
];

