
import React from 'react';
import { MapPin } from 'lucide-react';
import { FormData } from '../../types/plan';

interface DestinationSectionProps {
  formData: FormData;
  setFormData: React.Dispatch<React.SetStateAction<FormData>>;
}

const DestinationSection: React.FC<DestinationSectionProps> = ({ formData, setFormData }) => {
  return (
    <div className="card-elevated p-8">
      <h2 className="flex-center text-subheading mb-6">
        <MapPin className="text-primary" size={24} />
        <span>Where are you traveling?</span>
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-muted-foreground mb-2">From (Origin)</label>
          <input
            type="text"
            value={formData.from}
            onChange={(e) => setFormData({...formData, from: e.target.value})}
            placeholder="Delhi"
            className="w-full px-4 py-3 bg-muted border border-border rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-foreground theme-transition"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-muted-foreground mb-2">To (Destination)</label>
          <input
            type="text"
            value={formData.to}
            onChange={(e) => setFormData({...formData, to: e.target.value})}
            placeholder="Kolkata"
            className="w-full px-4 py-3 bg-muted border border-border rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-foreground theme-transition"
          />
        </div>
      </div>
    </div>
  );
};

export default DestinationSection;
