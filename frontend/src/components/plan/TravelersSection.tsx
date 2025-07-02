
import React from 'react';
import { FormData } from '../../types/plan';
import { travelerOptions } from '../../data/planOptions';

interface TravelersSectionProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const TravelersSection: React.FC<TravelersSectionProps> = ({ formData, setFormData }) => {
  return (
    <div className="card-elevated p-8">
      <h2 className="text-subheading mb-6 text-center">
        Who do you plan on traveling with on your next adventure?
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {travelerOptions.map((option) => (
          <label key={option.value} className="cursor-pointer">
            <input
              type="radio"
              name="travelers"
              value={option.value}
              checked={formData.travelers === option.value}
              onChange={(e) => setFormData({...formData, travelers: e.target.value})}
              className="sr-only"
            />
            <div className={`p-6 rounded-xl border-2 transition-all duration-200 text-center hover-lift theme-transition ${
              formData.travelers === option.value
                ? 'border-primary gradient-saffron text-white shadow-lg'
                : 'border-border hover:border-primary/50 hover:shadow-md'
            }`}>
              <div className="text-3xl mb-3">{option.icon}</div>
              <div className="text-lg font-medium mb-1">{option.label}</div>
              <div className="text-sm opacity-80">{option.description}</div>
            </div>
          </label>
        ))}
      </div>
    </div>
  );
};

export default TravelersSection;
