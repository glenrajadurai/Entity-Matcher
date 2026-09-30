import React, { useState } from 'react';
import { Sidebar, NavTab } from './components/Sidebar';
import { DashboardOverview } from './components/DashboardOverview';
import { DataOverviewPage } from './components/DataOverviewPage';
import { ModelPerformancePage } from './components/ModelPerformancePage';
import { ErrorAnalysisPage } from './components/ErrorAnalysisPage';
import { ResearchImprovementPage } from './components/ResearchImprovementPage';
import { EntityMatchingDemo } from './components/EntityMatchingDemo';
import { RobustnessPage } from './components/RobustnessPage';
import { FinalResultsPage } from './components/FinalResultsPage';
import { ArchitecturePage } from './components/ArchitecturePage';
import { TeamPage } from './components/TeamPage';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>('dashboard');

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardOverview />;
      case 'data-overview':
        return <DataOverviewPage />;
      case 'model-performance':
        return <ModelPerformancePage />;
      case 'error-analysis':
        return <ErrorAnalysisPage />;
      case 'research-improvement':
        return <ResearchImprovementPage />;
      case 'entity-matching':
        return <EntityMatchingDemo />;
      case 'robustness':
        return <RobustnessPage />;
      case 'final-results':
        return <FinalResultsPage />;
      case 'architecture':
        return <ArchitecturePage />;
      case 'team':
        return <TeamPage />;
      default:
        return <DashboardOverview />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0b0f19] text-slate-100">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="flex-1 p-8 overflow-y-auto max-w-7xl">
        {renderTabContent()}
      </main>
    </div>
  );
};

export default App;
