import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../providers/search_provider.dart';
import '../models/search_item.dart';

class SearchResultsScreen extends StatefulWidget {
  final int preferenceIndex;

  const SearchResultsScreen({
    super.key,
    required this.preferenceIndex,
  });

  @override
  State<SearchResultsScreen> createState() => _SearchResultsScreenState();
}

class _SearchResultsScreenState extends State<SearchResultsScreen> {
  @override
  void initState() {
    super.initState();
    // Start search on init
    Future.microtask(
      () => context.read<SearchProvider>().search(widget.preferenceIndex),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Search Results'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              context.read<SearchProvider>().search(widget.preferenceIndex);
            },
            tooltip: 'Search Again',
          ),
        ],
      ),
      body: Consumer<SearchProvider>(
        builder: (context, provider, child) {
          if (provider.isSearching) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Searching deals...'),
                ],
              ),
            );
          }

          if (provider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, size: 64, color: Colors.red),
                  const SizedBox(height: 16),
                  Text(
                    'Search error',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 8),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 32),
                    child: Text(
                      provider.error!,
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton.icon(
                    onPressed: () {
                      provider.search(widget.preferenceIndex);
                    },
                    icon: const Icon(Icons.refresh),
                    label: const Text('Tentar Novamente'),
                  ),
                ],
              ),
            );
          }

          if (provider.items.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.inbox, size: 64, color: Colors.grey),
                  const SizedBox(height: 16),
                  Text(
                    'Nenhum item encontrado',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 8),
                  const Text('Try adjusting your search filters'),
                ],
              ),
            );
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: provider.items.length,
            itemBuilder: (context, index) {
              return _SearchItemCard(item: provider.items[index]);
            },
          );
        },
      ),
    );
  }
}

class _SearchItemCard extends StatelessWidget {
  final SearchItem item;

  const _SearchItemCard({required this.item});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: InkWell(
        onTap: () => _openLink(item.link),
        borderRadius: BorderRadius.circular(20),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _CardMedia(item: item),
              const SizedBox(height: 16),
              Text(
                item.priceText.isNotEmpty ? item.priceText : item.title,
                style: theme.textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: theme.colorScheme.primary,
                ),
              ),
              if (item.priceText.isNotEmpty && item.title.isNotEmpty && item.priceText != item.title) ...[
                const SizedBox(height: 4),
                Text(
                  item.title,
                  style: theme.textTheme.titleMedium,
                ),
              ],
              const SizedBox(height: 8),
              Text(
                item.origin,
                style: theme.textTheme.labelLarge?.copyWith(letterSpacing: 1.1),
              ),
              if (item.extraInfo.isNotEmpty) ...[
                const SizedBox(height: 6),
                Text(
                  item.extraInfo,
                  style: theme.textTheme.bodySmall,
                ),
              ],
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => _openLink(item.link),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(999)),
                  ),
                  child: const Text('View deal'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _openLink(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }
}

class _CardMedia extends StatelessWidget {
  final SearchItem item;

  const _CardMedia({required this.item});

  @override
  Widget build(BuildContext context) {
    final badgeLabel = item.extraInfo.isNotEmpty ? item.extraInfo : item.origin;
    return Stack(
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: Container(
            width: double.infinity,
            height: 150,
            color: Colors.grey[200],
            child: item.imageUrl.isNotEmpty
                ? Image.network(
                    item.imageUrl,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) => const _PlaceholderImage(),
                  )
                : const _PlaceholderImage(),
          ),
        ),
        if (badgeLabel.isNotEmpty)
          Positioned(
            top: 12,
            left: 12,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: Colors.green[400],
                borderRadius: BorderRadius.circular(999),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.1),
                    blurRadius: 6,
                    offset: const Offset(0, 3),
                  ),
                ],
              ),
              child: Text(
                badgeLabel,
                style: Theme.of(context).textTheme.labelMedium?.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                    ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ),
      ],
    );
  }
}

class _PlaceholderImage extends StatelessWidget {
  const _PlaceholderImage();

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.grey[200],
      alignment: Alignment.center,
      child: Icon(
        Icons.image_outlined,
        size: 40,
        color: Colors.grey[500],
      ),
    );
  }
}



