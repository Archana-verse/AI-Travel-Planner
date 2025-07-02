
import React, { useState } from 'react';
import { Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { FormData } from '../../types/plan';
import DestinationSection from './DestinationSection';
import DateSection from './DateSection';
import TravelClassSection from './TravelClassSection';
import BudgetSection from './BudgetSection';
import TravelersSection from './TravelersSection';
import InterestsSection from './InterestsSection';
import DietarySection from './DietarySection';

const PlanForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    from: '',
    to: '',
    departureDate: '',
    returnDate: '',
    travelClass: 'economy',
    budget: '',
    travelers: 'solo',
    interests: [],
    diet: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Trip planning form submitted:', formData);
    navigate('/flights');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      <DestinationSection formData={formData} setFormData={setFormData} />
      <DateSection formData={formData} setFormData={setFormData} />
      <TravelClassSection formData={formData} setFormData={setFormData} />
      <BudgetSection formData={formData} setFormData={setFormData} />
      <TravelersSection formData={formData} setFormData={setFormData} />
      <InterestsSection formData={formData} setFormData={setFormData} />
      <DietarySection formData={formData} setFormData={setFormData} />

      <button
        type="submit"
        className="w-full btn-primary text-lg py-4 flex-center"
      >
        <Sparkles size={20} />
        <span>Find My Perfect Trip</span>
      </button>
    </form>  
  );
};

export default PlanForm;
