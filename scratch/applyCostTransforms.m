%% Transform Costs.  
% Create a second row of Costs cell array to hold transformed values.
% This allows easy retreival of original values for rescaling

disp([datestr(now,14),' Applying numerical transformations to edge costs.']);
for i=1:length(Costs)
    Costs{2,i}=Costs{1,i};
end
Costs{2,1}=Costs{2,1}./min(Costs{2,1}); % First is distance, scale to minimum value
for i=2:length(Costs)
    if (Options.Costs{i-1}.type==1)     % Apply Transformatin to Areal Slope
        if Options.defaultSlopeValues~=4
            Options.areaSteepness=.055;   %Changed from 0.03 on 1 october 2007 MJN
        end
        Costs{2,i}=exp(Options.areaSteepness*Costs{1,i}); %Apply scaling function for areal slope
    elseif (Options.Costs{i-1}.type==2)  % Apply Transformation to Linear Slope
        switch Options.typeLinearSlopeTransform
            case 1
                hikingFunction;
            case 2
                splinedAsymmetric;
        end
    else Costs{2,i}=Costs{1,i}; % All other cost surfaces leave untransformed
    end
end
clear i;

