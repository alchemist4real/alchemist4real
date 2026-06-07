const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, '../data.json');

async function sync() {
  console.log('Starting GitHub sync...');
  
  // Read local data.json
  let localData = { projects: [], extensions: [], research: [], repos: [] };
  if (fs.existsSync(DATA_FILE)) {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    localData = JSON.parse(raw);
  }

  // Flatten catalog
  let allCatalogItems = [
    ...(localData.projects || []).map(item => ({ ...item, type: 'projects' })),
    ...(localData.extensions || []).map(item => ({ ...item, type: 'extensions' })),
    ...(localData.research || []).map(item => ({ ...item, type: 'research' })),
    ...(localData.repos || []).map(item => ({ ...item, type: 'repos' }))
  ];

  try {
    const res = await fetch('https://api.github.com/users/alchemist4real/repos?per_page=100&sort=updated', {
      headers: {
        'User-Agent': 'alchemist4real-sync-bot'
      }
    });

    if (!res.ok) {
      throw new Error(`GitHub API returned ${res.status} ${res.statusText}`);
    }

    const ghData = await res.json();
    const existingLinks = new Set(allCatalogItems.map(item => (item.link || '').toLowerCase().replace(/\/$/, '')));
    const existingTitles = new Set(allCatalogItems.map(item => (item.title || '').toLowerCase()));

    ghData.forEach(repo => {
      const url1 = (repo.homepage || '').toLowerCase().replace(/\/$/, '');
      const url2 = (repo.html_url || '').toLowerCase().replace(/\/$/, '');
      
      const isExtension = 
        repo.name.toLowerCase().includes('extension') || 
        (repo.description && (repo.description.toLowerCase().includes('ekstensi') || repo.description.toLowerCase().includes('extension'))) ||
        (repo.topics && repo.topics.some(t => t.toLowerCase().includes('extension')));

      let isDuplicate = false;
      let matchedItem = null;
      
      if (url1 && existingLinks.has(url1)) {
        matchedItem = allCatalogItems.find(i => (i.link || '').toLowerCase().replace(/\/$/, '') === url1);
        if (matchedItem) {
          if (repo.html_url && matchedItem.link !== repo.html_url) matchedItem.repo_link = repo.html_url;
          // if (repo.description && repo.description !== matchedItem.description) matchedItem.description = repo.description.toLowerCase() + (repo.description.endsWith('.') ? '' : '.');
        }
        isDuplicate = true;
      }
      if (!isDuplicate && existingLinks.has(url2)) {
        matchedItem = allCatalogItems.find(i => (i.link || '').toLowerCase().replace(/\/$/, '') === url2);
        if (matchedItem) {
          if (repo.homepage && matchedItem.link !== repo.homepage) matchedItem.web_link = repo.homepage;
          // if (repo.description && repo.description !== matchedItem.description) matchedItem.description = repo.description.toLowerCase() + (repo.description.endsWith('.') ? '' : '.');
        }
        isDuplicate = true;
      }
      if (!isDuplicate && existingTitles.has(repo.name.toLowerCase())) {
        matchedItem = allCatalogItems.find(i => (i.title || '').toLowerCase() === repo.name.toLowerCase());
        if (matchedItem) {
           if (repo.html_url && matchedItem.link !== repo.html_url) matchedItem.repo_link = repo.html_url;
           if (repo.homepage && matchedItem.link !== repo.homepage) matchedItem.web_link = repo.homepage;
           // if (repo.description && repo.description !== matchedItem.description) matchedItem.description = repo.description.toLowerCase() + (repo.description.endsWith('.') ? '' : '.');
        }
        isDuplicate = true;
      }
      
      if (matchedItem && isExtension) {
        matchedItem.type = 'extensions';
      }
      
      if (isDuplicate) return;

      // Add new live repo
      allCatalogItems.push({
        id: "GH-" + repo.name.substring(0,3).toUpperCase(),
        title: repo.name.toUpperCase().replace(/-/g, ' '),
        description: repo.description ? repo.description.toLowerCase() + (repo.description.endsWith('.') ? '' : '.') : "auto-synced repository.",
        tags: repo.topics && repo.topics.length > 0 ? repo.topics.slice(0, 2) : (repo.language ? [repo.language] : ['Code']),
        link: repo.homepage || repo.html_url,
        type: isExtension ? 'extensions' : 'repos'
      });
    });

    console.log('GitHub sync successful. Rebuilding data.json...');

    // Re-pack into localData format
    const newData = { projects: [], extensions: [], research: [], repos: [] };
    
    allCatalogItems.forEach(item => {
      const type = item.type || 'repos';
      delete item.type; // remove internal property
      if (newData[type]) {
        newData[type].push(item);
      } else {
        newData.repos.push(item);
      }
    });

    fs.writeFileSync(DATA_FILE, JSON.stringify(newData, null, 2), 'utf8');
    console.log('Done!');

  } catch (err) {
    console.error('Failed to sync:', err);
    process.exit(1);
  }
}

sync();
