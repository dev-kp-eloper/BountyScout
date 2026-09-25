import { BountyOpportunity } from '../types/opportunity';

export class OpportunityValidator {
  public static validate(opportunity: BountyOpportunity): boolean {
    if (!opportunity.id || typeof opportunity.id !== 'string') return false;
    if (!opportunity.title || typeof opportunity.title !== 'string') return false;
    if (opportunity.url !== null && typeof opportunity.url !== 'string') return false;
    if (opportunity.repository !== null && typeof opportunity.repository !== 'string') return false;
    if (typeof opportunity.comments !== 'number') return false;
    if (!this.validateISODate(opportunity.lastUpdated)) return false;
    if (opportunity.bountyAmount !== null && (typeof opportunity.bountyAmount !== 'number' || opportunity.bountyAmount < 0)) return false;
    if (!opportunity.type || typeof opportunity.type !== 'string') return false;
    if (!['active', 'discarded', 'pending'].includes(opportunity.status)) return false;
    
    return true;
  }

  private static validateISODate(dateString: string): boolean {
    const date = new Date(dateString);
    return !isNaN(date.getTime());
  }
}