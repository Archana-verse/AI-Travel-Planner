import React from 'react';
import { Plane } from 'lucide-react';
import { FormData } from '../../types/plan';
import { travelClassOptions } from '../../data/planOptions';

interface TravelClassSectionProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const TravelClassSection: React.FC<TravelClassSectionProps> = ({ formData, setFormData }) => {
  return (
    <div className="card-elevated p-8">
      <h2 className="flex-center text-subheading mb-6">
        <Plane className="text-primary" size={24} />
        <span>Choose your travel class</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {travelClassOptions.map((option) => (
          <label key={option.value} className="cursor-pointer">
            <input
              type="radio"
              name="travelClass"
              value={option.value}
              checked={formData.travelClass === option.value}
              onChange={(e) => setFormData({...formData, travelClass: e.target.value})}
              className="sr-only"
            />
            <div className={`p-6 rounded-xl border-2 transition-all duration-200 theme-transition ${
              formData.travelClass === option.value
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

export default TravelClassSection;
