// Plant Lore Victorian Garden Interface
// JavaScript for text navigation, data display, and D3.js visualizations

let analysisData = null;

// Load analysis data on page load
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('analysis.json');
        analysisData = await response.json();
        console.log('Analysis data loaded:', analysisData);

        // Initialize interface
        populateFolkardView();
        populateShakespeareView();
        populateComparisonView();
        setupNavigation();

    } catch (error) {
        console.error('Error loading analysis data:', error);
        alert('Failed to load analysis data. Please ensure analysis.json exists.');
    }
});

// Navigation between views
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const views = document.querySelectorAll('.text-view');

    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const viewName = button.dataset.view;

            // Update active button
            navButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Show corresponding view
            views.forEach(view => view.style.display = 'none');
            document.getElementById(`view-${viewName}`).style.display = 'block';
        });
    });
}

// Populate Folkard view
function populateFolkardView() {
    const folkardData = analysisData.texts[0];

    // Statistics
    document.getElementById('folkard-total-words').textContent = folkardData.total_words.toLocaleString();
    document.getElementById('folkard-unique-words').textContent = folkardData.unique_words.toLocaleString();
    document.getElementById('folkard-lexical-diversity').textContent = (folkardData.lexical_diversity * 100).toFixed(2) + '%';

    // Sentiment
    const sent = folkardData.sentiment;
    document.getElementById('folkard-sent-pos').style.width = (sent.positive * 100) + '%';
    document.getElementById('folkard-sent-pos-val').textContent = (sent.positive * 100).toFixed(1) + '%';

    document.getElementById('folkard-sent-neg').style.width = (sent.negative * 100) + '%';
    document.getElementById('folkard-sent-neg-val').textContent = (sent.negative * 100).toFixed(1) + '%';

    document.getElementById('folkard-sent-neu').style.width = (sent.neutral * 100) + '%';
    document.getElementById('folkard-sent-neu-val').textContent = (sent.neutral * 100).toFixed(1) + '%';

    document.getElementById('folkard-sent-compound').textContent = sent.compound.toFixed(3);

    // Top words
    const topWordsContainer = document.getElementById('folkard-top-words');
    folkardData.top_words.slice(0, 30).forEach(item => {
        const wordDiv = document.createElement('div');
        wordDiv.className = 'word-item';
        wordDiv.innerHTML = `
            <span class="word-text">${item.word}</span>
            <span class="word-count">${item.count}</span>
        `;
        topWordsContainer.appendChild(wordDiv);
    });
}

// Populate Shakespeare view
function populateShakespeareView() {
    const shakespeareData = analysisData.texts[1];

    // Statistics
    document.getElementById('shakespeare-total-words').textContent = shakespeareData.total_words.toLocaleString();
    document.getElementById('shakespeare-unique-words').textContent = shakespeareData.unique_words.toLocaleString();
    document.getElementById('shakespeare-lexical-diversity').textContent = (shakespeareData.lexical_diversity * 100).toFixed(2) + '%';

    // Sentiment
    const sent = shakespeareData.sentiment;
    document.getElementById('shakespeare-sent-pos').style.width = (sent.positive * 100) + '%';
    document.getElementById('shakespeare-sent-pos-val').textContent = (sent.positive * 100).toFixed(1) + '%';

    document.getElementById('shakespeare-sent-neg').style.width = (sent.negative * 100) + '%';
    document.getElementById('shakespeare-sent-neg-val').textContent = (sent.negative * 100).toFixed(1) + '%';

    document.getElementById('shakespeare-sent-neu').style.width = (sent.neutral * 100) + '%';
    document.getElementById('shakespeare-sent-neu-val').textContent = (sent.neutral * 100).toFixed(1) + '%';

    document.getElementById('shakespeare-sent-compound').textContent = sent.compound.toFixed(3);

    // Top words
    const topWordsContainer = document.getElementById('shakespeare-top-words');
    shakespeareData.top_words.slice(0, 30).forEach(item => {
        const wordDiv = document.createElement('div');
        wordDiv.className = 'word-item';
        wordDiv.innerHTML = `
            <span class="word-text">${item.word}</span>
            <span class="word-count">${item.count}</span>
        `;
        topWordsContainer.appendChild(wordDiv);
    });
}

// Populate Comparison view
function populateComparisonView() {
    const comparison = analysisData.comparison;

    // Overlap statistics
    document.getElementById('overlap-percent').textContent = comparison.overlap_percentage.toFixed(2) + '%';
    document.getElementById('overlap-detail').textContent =
        `${comparison.total_shared_words.toLocaleString()} shared words • ` +
        `${comparison.unique_to_folkard.toLocaleString()} unique to Folkard • ` +
        `${comparison.unique_to_shakespeare.toLocaleString()} unique to Shakespeare`;

    // Create Venn diagram visualization
    createVennDiagram(comparison);

    // Shared words
    const sharedWordsContainer = document.getElementById('shared-words');
    comparison.top_shared_words.slice(0, 30).forEach(item => {
        const wordDiv = document.createElement('div');
        wordDiv.className = 'word-item';
        wordDiv.innerHTML = `
            <span class="word-text">${item.word}</span>
            <span class="word-count">${item.combined_count}</span>
        `;
        sharedWordsContainer.appendChild(wordDiv);
    });
}

// Create Venn Diagram with D3.js
function createVennDiagram(comparison) {
    const container = document.getElementById('overlap-chart');
    const width = 600;
    const height = 400;

    // Clear existing content
    container.innerHTML = '';

    const svg = d3.select('#overlap-chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', `0 0 ${width} ${height}`)
        .style('max-width', '100%')
        .style('height', 'auto');

    // Venn diagram circles
    const radius = 120;
    const circleSpacing = 80;

    // Folkard circle (left)
    const folkardX = width / 2 - circleSpacing;
    const folkardY = height / 2;

    // Shakespeare circle (right)
    const shakespeareX = width / 2 + circleSpacing;
    const shakespeareY = height / 2;

    // Draw circles
    svg.append('circle')
        .attr('cx', folkardX)
        .attr('cy', folkardY)
        .attr('r', radius)
        .attr('class', 'venn-circle')
        .style('fill', '#8A9A8B'); // Sage green

    svg.append('circle')
        .attr('cx', shakespeareX)
        .attr('cy', shakespeareY)
        .attr('r', radius)
        .attr('class', 'venn-circle')
        .style('fill', '#B08F8F'); // Dusty rose

    // Labels
    svg.append('text')
        .attr('x', folkardX - 70)
        .attr('y', folkardY - radius - 20)
        .attr('class', 'venn-label')
        .attr('text-anchor', 'middle')
        .text('Folkard');

    svg.append('text')
        .attr('x', shakespeareX + 70)
        .attr('y', shakespeareY - radius - 20)
        .attr('class', 'venn-label')
        .attr('text-anchor', 'middle')
        .text('Shakespeare');

    // Counts
    svg.append('text')
        .attr('x', folkardX - 70)
        .attr('y', folkardY)
        .attr('class', 'venn-count')
        .attr('text-anchor', 'middle')
        .text(comparison.unique_to_folkard.toLocaleString());

    svg.append('text')
        .attr('x', shakespeareX + 70)
        .attr('y', shakespeareY)
        .attr('class', 'venn-count')
        .attr('text-anchor', 'middle')
        .text(comparison.unique_to_shakespeare.toLocaleString());

    // Overlap count
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', height / 2)
        .attr('class', 'venn-count')
        .attr('text-anchor', 'middle')
        .style('fill', '#6B394A') // Burgundy
        .text(comparison.total_shared_words.toLocaleString());

    svg.append('text')
        .attr('x', width / 2)
        .attr('y', height / 2 + 30)
        .attr('class', 'venn-label')
        .attr('text-anchor', 'middle')
        .style('font-size', '12px')
        .text('Shared');
}
