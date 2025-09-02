import React from 'react';
import { Slider } from '../ui/slider';
import { Hotel } from 'lucide-react';
import { FormData } from '../../types/plan';

interface HotelAffordabilitySliderProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const levels = ['low', 'medium', 'high'] as const;

const HotelAffordabilitySlider: React.FC<HotelAffordabilitySliderProps> = ({ formData, setFormData }) => {
  const valueIndex = levels.indexOf(formData.hotelAffordability);

  const handleChange = (val: number[]) => {
    const level = levels[val[0]];
    setFormData({ ...formData, hotelAffordability: level });
  };

  return (
    <div className="card-elevated p-8">
      <h2 className="flex-center text-subheading mb-6">
        <Hotel className="text-primary" size={24} />
        <span>Hotel Affordability Preference</span>
      </h2>
      
      <Slider
        min={0}
        max={2}
        step={1}
        defaultValue={[valueIndex]}
        value={[valueIndex]}
        onValueChange={handleChange}
        className="w-full"
      />

      <div className="flex justify-between mt-4 text-xs font-medium text-muted-foreground px-1">
        <span className={formData.hotelAffordability === 'low' ? 'text-primary font-semibold' : ''}>Low</span>
        <span className={formData.hotelAffordability === 'medium' ? 'text-primary font-semibold' : ''}>Medium</span>
        <span className={formData.hotelAffordability === 'high' ? 'text-primary font-semibold' : ''}>High</span>
      </div>
    </div>
  );
};

export default HotelAffordabilitySlider;
