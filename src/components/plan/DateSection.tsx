
import React from 'react';
import { Calendar } from 'lucide-react';
import { FormData } from '../../types/plan';

interface DateSectionProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const DateSection: React.FC<DateSectionProps> = ({ formData, setFormData }) => {
  return (
    <div className="card-elevated p-8">
      <h2 className="flex-center text-subheading mb-6">
        <Calendar className="text-primary" size={24} />
        <span>When are you traveling?</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-muted-foreground mb-2">Departure Date</label>
          <input
            type="date"
            value={formData.departureDate}
            onChange={(e) => setFormData({...formData, departureDate: e.target.value})}
            className="w-full px-4 py-3 bg-muted border border-border rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-foreground theme-transition"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-muted-foreground mb-2">Return Date</label>
          <input
            type="date"
            value={formData.returnDate}
            onChange={(e) => setFormData({...formData, returnDate: e.target.value})}
            className="w-full px-4 py-3 bg-muted border border-border rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-foreground theme-transition"
          />
        </div>
      </div>
    </div>
  );
};

export default DateSection;
