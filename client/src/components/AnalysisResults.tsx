import React from 'react';
import { FileText, Search, Image, ExternalLink, TrendingUp, AlertTriangle } from 'lucide-react';
import { AnalysisResults as AnalysisResultsType } from '../types';

interface AnalysisResultsProps {
  results: AnalysisResultsType;
  url: string;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results, url }) => {
  const { htmlContent, seoAnalysis, imageGeneration } = results;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 text-primary-600 hover:text-primary-700"
          >
            <ExternalLink className="w-4 h-4" />
            <span className="text-sm">Visit Site</span>
          </a>
        </div>
        <p className="text-gray-600 break-all">{url}</p>
      </div>

      {/* SEO Analysis */}
      {seoAnalysis && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-green-100 p-2 rounded-lg">
              <TrendingUp className="w-5 h-5 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">SEO Analysis</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-3xl font-bold text-primary-600 mb-1">
                {seoAnalysis.seo_score}%
              </div>
              <div className="text-sm text-gray-600">SEO Score</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-3xl font-bold text-green-600 mb-1">
                {seoAnalysis.passed_checks}
              </div>
              <div className="text-sm text-gray-600">Passed Checks</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-3xl font-bold text-red-600 mb-1">
                {seoAnalysis.issues.length}
              </div>
              <div className="text-sm text-gray-600">Issues Found</div>
            </div>
          </div>

          {seoAnalysis.issues.length > 0 && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                <AlertTriangle className="w-4 h-4 text-red-500 mr-2" />
                Issues
              </h4>
              <ul className="space-y-1">
                {seoAnalysis.issues.slice(0, 5).map((issue, index) => (
                  <li key={index} className="text-sm text-red-600">• {issue}</li>
                ))}
              </ul>
            </div>
          )}

          {seoAnalysis.recommendations.length > 0 && (
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900 mb-2">Recommendations</h4>
              <ul className="space-y-1">
                {seoAnalysis.recommendations.slice(0, 5).map((rec, index) => (
                  <li key={index} className="text-sm text-green-600">• {rec}</li>
                ))}
              </ul>
            </div>
          )}

          {seoAnalysis.keywords.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">Top Keywords</h4>
              <div className="flex flex-wrap gap-2">
                {seoAnalysis.keywords.slice(0, 10).map((keyword, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* HTML Content */}
      {htmlContent && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-blue-100 p-2 rounded-lg">
              <FileText className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">HTML Content Analysis</h3>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {htmlContent.total_elements}
              </div>
              <div className="text-sm text-gray-600">Total Elements</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {htmlContent.headings ? Object.values(htmlContent.headings).flat().length : 0}
              </div>
              <div className="text-sm text-gray-600">Headings</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {htmlContent.paragraphs.length}
              </div>
              <div className="text-sm text-gray-600">Paragraphs</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {htmlContent.divisions.length}
              </div>
              <div className="text-sm text-gray-600">Divisions</div>
            </div>
          </div>

          {htmlContent.summary && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-2">Content Summary</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Content Density: </span>
                  <span className="font-medium text-gray-900 capitalize">
                    {htmlContent.summary.content_density}
                  </span>
                </div>
                <div>
                  <span className="text-gray-600">Structural Complexity: </span>
                  <span className="font-medium text-gray-900 capitalize">
                    {htmlContent.summary.structural_complexity}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Image Generation */}
      {imageGeneration && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-purple-100 p-2 rounded-lg">
              <Image className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">Image Analysis</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {imageGeneration.total_images}
              </div>
              <div className="text-sm text-gray-600">Total Images</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {imageGeneration.processed_images}
              </div>
              <div className="text-sm text-gray-600">Processed Images</div>
            </div>
          </div>

          {imageGeneration.alt_text_suggestions && imageGeneration.alt_text_suggestions.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Alt Text Suggestions</h4>
              <div className="space-y-3">
                {imageGeneration.alt_text_suggestions.slice(0, 3).map((suggestion, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-3">
                    <div className="text-sm text-gray-600 mb-1">Image {suggestion.image_index}</div>
                    <div className="text-sm">
                      <span className="font-medium">Suggested: </span>
                      <span className="text-gray-900">{suggestion.suggested_alt}</span>
                    </div>
                    {suggestion.current_alt && (
                      <div className="text-sm mt-1">
                        <span className="font-medium">Current: </span>
                        <span className="text-gray-600">{suggestion.current_alt}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;
