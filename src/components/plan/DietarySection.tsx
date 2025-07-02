
import React from 'react';
import { Utensils } from 'lucide-react';
import { FormData } from '../../types/plan';

interface DietarySectionProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const DietarySection: React.FC<DietarySectionProps> = ({ formData, setFormData }) => {
  return (
    <div className="card-elevated p-8">
      <h2 className="flex-center text-subheading mb-6">
        <Utensils className="text-primary" size={24} />
        <span>Dietary Preference</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label className="cursor-pointer">
          <input
            type="radio"
            name="diet"
            value="vegetarian"
            checked={formData.diet === 'vegetarian'}
            onChange={(e) => setFormData({...formData, diet: e.target.value})}
            className="sr-only"
          />
          <div className={`p-6 rounded-xl border-2 transition-all duration-200 hover-lift theme-transition ${
            formData.diet === 'vegetarian'
              ? 'border-primary gradient-saffron text-white shadow-lg'
              : 'border-border hover:border-primary/50 hover:shadow-md'
          }`}>
            <div className="flex-center">
              <span className="text-2xl">🥬</span>
              <div>
                <div className="font-medium">Vegetarian</div>
                <div className="text-sm opacity-80">Plant-based meals only</div>
              </div>
            </div>
          </div>
        </label>
        <label className="cursor-pointer">
          <input
            type="radio"
            name="diet"
            value="non-vegetarian"
            checked={formData.diet === 'non-vegetarian'}
            onChange={(e) => setFormData({...formData, diet: e.target.value})}
            className="sr-only"
          />
          <div className={`p-6 rounded-xl border-2 transition-all duration-200 hover-lift theme-transition ${
            formData.diet === 'non-vegetarian'
              ? 'border-primary gradient-saffron text-white shadow-lg'
              : 'border-border hover:border-primary/50 hover:shadow-md'
          }`}>
            <div className="flex-center">
              <span className="text-2xl">🍖</span>
              <div>
                <div className="font-medium">Non-Vegetarian</div>
                <div className="text-sm opacity-80">All food options</div>
              </div>
            </div>
          </div>
        </label>
      </div>
    </div>
  );
};

export default DietarySection;
