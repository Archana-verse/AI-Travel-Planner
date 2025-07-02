
import React from 'react';
import { DollarSign } from 'lucide-react';
import { FormData } from '../../types/plan';
import { budgetOptions } from '../../data/planOptions';

interface BudgetSectionProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const BudgetSection: React.FC<BudgetSectionProps> = ({ formData, setFormData }) => {
  return (
    <div className="card-elevated p-8">
      <h2 className="flex-center text-subheading mb-6">
        <DollarSign className="text-primary" size={24} />
        <span>What's your budget range?</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {budgetOptions.map((option) => (
          <label key={option.value} className="cursor-pointer">
            <input
              type="radio"
              name="budget"
              value={option.value}
              checked={formData.budget === option.value}
              onChange={(e) => setFormData({...formData, budget: e.target.value})}
              className="sr-only"
            />
            <div className={`p-6 rounded-xl border-2 transition-all duration-200 hover-lift theme-transition ${
              formData.budget === option.value
                ? 'border-primary gradient-saffron text-white shadow-lg'
                : 'border-border hover:border-primary/50 hover:shadow-md'
            }`}>
              <div className="text-lg font-medium mb-1">{option.label}</div>
              <div className="text-sm opacity-80">{option.subtitle}</div>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
};

export default BudgetSection;
