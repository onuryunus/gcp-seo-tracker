import React from 'react';
import DonutChart from './charts/DonutChart';
import ProgressBar from './charts/ProgressBar';
import KeywordChart from './charts/KeywordChart';
import MetricsCard from './cards/MetricsCard';
import IssuesCard from './cards/IssuesCard';
import { 
  TrendingUp, 
  Search, 
  Image, 
  FileText, 
  CheckCircle,
  Target,
  BarChart3
} from 'lucide-react';

interface Keyword {
  word: string;
  count: number;
  percentage: number;
}

interface AnalysisResult {
  status: string;
  url: string;
  seo_score: number;
  total_checks: number;
  passed_checks: number;
  issues: string[];
  recommendations: string[];
  keywords: Keyword[];
  detailed_report: string;
  page_info: {
    title: string;
    meta_description: string;
    word_count: number;
    headings_count: Record<string, number>;
    images_total: number;
    images_with_alt: number;
  };
}

interface DashboardProps {
  result: AnalysisResult;
  url: string;
  className?: string;
}

const Dashboard: React.FC<DashboardProps> = ({
  result,
  url,
  className = ''
}) => {
  // Calculate summary metrics from the flat structure
  const seoScore = result.seo_score || 0;
  const totalChecks = result.total_checks || 0;
  const passedChecks = result.passed_checks || 0;
  const totalImages = result.page_info?.images_total || 0;
  const processedImages = result.page_info?.images_with_alt || 0;
  const wordCount = result.page_info?.word_count || 0;

  // Get color based on score
  const getScoreColor = (score: number): 'green' | 'yellow' | 'red' => {
    if (score >= 80) return 'green';
    if (score >= 60) return 'yellow';
    return 'red';
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Dashboard</h2>
            <p className="text-gray-600">{url}</p>
            <p className="text-sm text-gray-500 mt-1">
              Analysis completed on {new Date().toLocaleDateString()}
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-blue-600">{seoScore}/100</div>
            <div className="text-sm text-gray-600">SEO Score</div>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricsCard
          title="SEO Score"
          value={seoScore}
          subtitle={`${passedChecks}/${totalChecks} checks passed`}
          icon={TrendingUp}
          color={getScoreColor(seoScore)}
        >
          <ProgressBar 
            value={passedChecks} 
            max={totalChecks} 
            showPercentage={false}
            color={getScoreColor(seoScore)}
          />
        </MetricsCard>

        <MetricsCard
          title="Word Count"
          value={wordCount}
          subtitle="Total words analyzed"
          icon={FileText}
          color="blue"
        />

        <MetricsCard
          title="Keywords Found"
          value={result.keywords?.length || 0}
          subtitle="Unique keywords identified"
          icon={Search}
          color="purple"
        />

        <MetricsCard
          title="Images"
          value={totalImages}
          subtitle={`${processedImages} processed`}
          icon={Image}
          color="gray"
        >
          {totalImages > 0 && (
            <ProgressBar 
              value={processedImages} 
              max={totalImages} 
              showPercentage={false}
              color="blue"
            />
          )}
        </MetricsCard>
      </div>

      {/* SEO Score Visualization */}
      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* SEO Score Donut Chart */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Target className="w-5 h-5" />
              SEO Performance
            </h3>
            <div className="flex justify-center">
              <DonutChart 
                score={seoScore} 
                size={200}
                colors={{
                  filled: seoScore >= 80 ? '#10B981' : seoScore >= 60 ? '#F59E0B' : '#EF4444',
                  empty: '#E5E7EB'
                }}
              />
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <BarChart3 className="w-5 h-5" />
              Quick Stats
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Total Checks</span>
                <span className="font-semibold">{totalChecks}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Passed</span>
                <span className="font-semibold text-green-600">{passedChecks}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Issues</span>
                <span className="font-semibold text-red-600">{result.issues?.length || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Recommendations</span>
                <span className="font-semibold text-blue-600">{result.recommendations?.length || 0}</span>
              </div>
            </div>
          </div>

          {/* Status Indicators */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Overview</h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <div>
                  <div className="font-medium">Analysis Status</div>
                  <div className="text-sm text-gray-600">
                    {result.status || 'Completed'}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <div>
                  <div className="font-medium">Page Title</div>
                  <div className="text-sm text-gray-600">
                    {result.page_info?.title || 'Not available'}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <div>
                  <div className="font-medium">Meta Description</div>
                  <div className="text-sm text-gray-600">
                    {result.page_info?.meta_description ? 'Available' : 'Not available'}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Keywords Chart */}
      {result.keywords && result.keywords.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Search className="w-5 h-5" />
            Top Keywords
          </h3>
          <KeywordChart keywords={result.keywords} height={300} />
        </div>
      )}

      {/* Issues and Recommendations */}
      {(result.issues?.length > 0 || result.recommendations?.length > 0) && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {result.issues && result.issues.length > 0 && (
            <IssuesCard
              title="SEO Issues"
              issues={result.issues}
              type="issues"
            />
          )}

          {result.recommendations && result.recommendations.length > 0 && (
            <IssuesCard
              title="Recommendations"
              issues={result.recommendations}
              type="recommendations"
            />
          )}
        </div>
      )}

      {/* Detailed Report */}
      {result.detailed_report && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Detailed SEO Analysis Report
          </h3>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 whitespace-pre-wrap">
              {result.detailed_report}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
