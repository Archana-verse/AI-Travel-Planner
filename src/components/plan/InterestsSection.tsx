
import React from 'react';
import { Heart } from 'lucide-react';
import { FormData } from '../../types/plan';
import { interestOptions } from '../../data/planOptions';

interface InterestsSectionProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const InterestsSection: React.FC<InterestsSectionProps> = ({ formData, setFormData }) => {
  const handleInterestToggle = (interestId: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interestId)
        ? prev.interests.filter(id => id !== interestId)
        : [...prev.interests, interestId]
    }));
  };

  return (
    <div className="card-elevated p-8">
      <h2 className="flex-center text-subheading mb-6">
        <Heart className="text-primary" size={24} />
        <span>What interests you? (Select multiple)</span>
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {interestOptions.map((interest) => (
          <button
            key={interest.id}
            type="button"
            onClick={() => handleInterestToggle(interest.id)}
            className={`p-4 rounded-xl border-2 transition-all duration-200 hover-lift theme-transition ${
              formData.interests.includes(interest.id)
                ? 'border-primary gradient-saffron text-white shadow-lg'
                : 'border-border hover:border-primary/50 hover:shadow-md'
            }`}
          >
            <div className="text-2xl mb-2">{interest.icon}</div>
            <div className="text-sm font-medium">{interest.label}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default InterestsSection;
