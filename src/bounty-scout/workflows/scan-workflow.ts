import { BountyScanner } from '../services/scanner';
import { OpportunityValidator } from '../validators/opportunity';
import { groupByRepository } from '../utils/array';
import { BountyOpportunity } from '../types/opportunity';

export class ScanWorkflow {
  public static async execute(rawIssues: any[]): Promise<BountyOpportunity[]> {
    const scanner = new BountyScanner();
    const opportunities = await scanner.scanIssues(rawIssues);
    
    const validated = opportunities.filter(opportunity => {
      return OpportunityValidator.validate(opportunity);
    });
    
    return validated;
  }

  public static async executeWithGrouping(rawIssues: any[]): Promise<Record<string, BountyOpportunity[]>> {
    const opportunities = await this.execute(rawIssues);
    return groupByRepository(opportunities);
  }
}