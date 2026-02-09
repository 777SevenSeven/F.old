import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/user_preference.dart';
import '../models/source_config.dart';
import '../providers/preferences_provider.dart';

class PreferenceFormScreen extends StatefulWidget {
  final UserPreference? preference;
  final int? index;

  const PreferenceFormScreen({
    super.key,
    this.preference,
    this.index,
  });

  @override
  State<PreferenceFormScreen> createState() => _PreferenceFormScreenState();
}

class _PreferenceFormScreenState extends State<PreferenceFormScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _chatIdController;
  late TextEditingController _productController;
  late TextEditingController _cityController;
  late TextEditingController _minPriceController;
  late TextEditingController _maxPriceController;
  late TextEditingController _negativeKeywordsController;
  late TextEditingController _facebookUrlController;
  late TextEditingController _mercadoLivreUrlController;
  late TextEditingController _olxUrlController;

  bool _facebookActive = false;
  bool _mercadoLivreActive = false;
  bool _olxActive = false;

  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    
    final pref = widget.preference;
    _chatIdController = TextEditingController(text: pref?.chatId ?? '');
    _productController = TextEditingController(text: pref?.product ?? '');
    _cityController = TextEditingController(text: pref?.targetCity ?? '');
    _minPriceController = TextEditingController(
      text: pref?.minPrice.toString() ?? '0',
    );
    _maxPriceController = TextEditingController(
      text: pref?.maxPrice.toString() ?? '999999',
    );
    _negativeKeywordsController = TextEditingController(
      text: pref?.negativeKeywords.join(', ') ?? '',
    );
    _facebookUrlController = TextEditingController(
      text: pref?.facebook.url ?? '',
    );
    _mercadoLivreUrlController = TextEditingController(
      text: pref?.mercadoLivre.url ?? '',
    );
    _olxUrlController = TextEditingController(text: pref?.olx.url ?? '');

    _facebookActive = pref?.facebook.active ?? false;
    _mercadoLivreActive = pref?.mercadoLivre.active ?? false;
    _olxActive = pref?.olx.active ?? false;
  }

  @override
  void dispose() {
    _chatIdController.dispose();
    _productController.dispose();
    _cityController.dispose();
    _minPriceController.dispose();
    _maxPriceController.dispose();
    _negativeKeywordsController.dispose();
    _facebookUrlController.dispose();
    _mercadoLivreUrlController.dispose();
    _olxUrlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isEditing = widget.preference != null;

    return Scaffold(
      appBar: AppBar(
        title: Text(isEditing ? 'Edit Search' : 'New Search'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Chat ID
            TextFormField(
              controller: _chatIdController,
              decoration: const InputDecoration(
                labelText: 'Chat ID (Telegram)',
                hintText: 'Telegram chat ID',
                prefixIcon: Icon(Icons.telegram),
              ),
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Required field';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),

            // Product
            TextFormField(
              controller: _productController,
              decoration: const InputDecoration(
                labelText: 'Product',
                hintText: 'e.g. iPhone 13, Bicycle',
                prefixIcon: Icon(Icons.shopping_bag),
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Required field';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),

            // City
            TextFormField(
              controller: _cityController,
              decoration: const InputDecoration(
                labelText: 'City',
                hintText: 'e.g. Sao Paulo',
                prefixIcon: Icon(Icons.location_city),
              ),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Required field';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),

            // Price Range
            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _minPriceController,
                    decoration: const InputDecoration(
                      labelText: 'Min Price',
                      prefixIcon: Icon(Icons.attach_money),
                    ),
                    keyboardType: TextInputType.number,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Required';
                      }
                      if (int.tryParse(value) == null) {
                        return 'Invalid number';
                      }
                      return null;
                    },
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: TextFormField(
                    controller: _maxPriceController,
                    decoration: const InputDecoration(
                      labelText: 'Max Price',
                      prefixIcon: Icon(Icons.attach_money),
                    ),
                    keyboardType: TextInputType.number,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Required';
                      }
                      if (int.tryParse(value) == null) {
                        return 'Invalid number';
                      }
                      return null;
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Negative Keywords
            TextFormField(
              controller: _negativeKeywordsController,
              decoration: const InputDecoration(
                labelText: 'Negative keywords (comma-separated)',
                hintText: 'e.g. broken, scratched',
                prefixIcon: Icon(Icons.block),
              ),
              maxLines: 2,
            ),
            const SizedBox(height: 24),

            // Sources Section
            Text(
              'Search Sources',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),

            // Facebook
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    SwitchListTile(
                      title: const Text('Facebook Marketplace'),
                      value: _facebookActive,
                      onChanged: (value) {
                        setState(() {
                          _facebookActive = value;
                        });
                      },
                      contentPadding: EdgeInsets.zero,
                    ),
                    if (_facebookActive) ...[
                      const SizedBox(height: 8),
                      TextFormField(
                        controller: _facebookUrlController,
                        decoration: const InputDecoration(
                          labelText: 'Search URL',
                          hintText: 'Paste the Facebook Marketplace URL',
                        ),
                        validator: _facebookActive
                            ? (value) {
                                if (value == null || value.isEmpty) {
                                  return 'URL is required';
                                }
                                return null;
                              }
                            : null,
                      ),
                    ],
                  ],
                ),
              ),
            ),
            const SizedBox(height: 12),

            // Mercado Livre
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    SwitchListTile(
                      title: const Text('Mercado Livre'),
                      value: _mercadoLivreActive,
                      onChanged: (value) {
                        setState(() {
                          _mercadoLivreActive = value;
                        });
                      },
                      contentPadding: EdgeInsets.zero,
                    ),
                    if (_mercadoLivreActive) ...[
                      const SizedBox(height: 8),
                      TextFormField(
                        controller: _mercadoLivreUrlController,
                        decoration: const InputDecoration(
                          labelText: 'Search URL',
                          hintText: 'Paste the Mercado Livre URL',
                        ),
                        validator: _mercadoLivreActive
                            ? (value) {
                                if (value == null || value.isEmpty) {
                                  return 'URL is required';
                                }
                                return null;
                              }
                            : null,
                      ),
                    ],
                  ],
                ),
              ),
            ),
            const SizedBox(height: 12),

            // OLX
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    SwitchListTile(
                      title: const Text('OLX'),
                      value: _olxActive,
                      onChanged: (value) {
                        setState(() {
                          _olxActive = value;
                        });
                      },
                      contentPadding: EdgeInsets.zero,
                    ),
                    if (_olxActive) ...[
                      const SizedBox(height: 8),
                      TextFormField(
                        controller: _olxUrlController,
                        decoration: const InputDecoration(
                          labelText: 'Search URL',
                          hintText: 'Paste the OLX URL',
                        ),
                        validator: _olxActive
                            ? (value) {
                                if (value == null || value.isEmpty) {
                                  return 'URL is required';
                                }
                                return null;
                              }
                            : null,
                      ),
                    ],
                  ],
                ),
              ),
            ),
            const SizedBox(height: 32),

            // Save Button
            ElevatedButton.icon(
              onPressed: _isLoading ? null : _savePreference,
              icon: _isLoading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.save),
              label: Text(isEditing ? 'Update' : 'Save'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _savePreference() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    final negativeKeywords = _negativeKeywordsController.text
        .split(',')
        .map((e) => e.trim())
        .where((e) => e.isNotEmpty)
        .toList();

    final preference = UserPreference(
      chatId: _chatIdController.text,
      product: _productController.text,
      targetCity: _cityController.text,
      minPrice: int.parse(_minPriceController.text),
      maxPrice: int.parse(_maxPriceController.text),
      negativeKeywords: negativeKeywords,
      facebook: SourceConfig(
        active: _facebookActive,
        url: _facebookUrlController.text,
      ),
      mercadoLivre: SourceConfig(
        active: _mercadoLivreActive,
        url: _mercadoLivreUrlController.text,
      ),
      olx: SourceConfig(
        active: _olxActive,
        url: _olxUrlController.text,
      ),
    );

    final provider = context.read<PreferencesProvider>();
    bool success;

    if (widget.index != null) {
      success = await provider.updatePreference(widget.index!, preference);
    } else {
      success = await provider.addPreference(preference);
    }

    setState(() {
      _isLoading = false;
    });

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            widget.index != null
                ? 'Preference updated!'
                : 'Preference created!',
          ),
          backgroundColor: Colors.green,
        ),
      );
      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error: ${provider.error ?? "Unknown"}'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }
}


