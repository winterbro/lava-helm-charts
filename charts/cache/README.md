# Lava Provider Cache Helm Chart

Running a lava provider cache on Kubernetes is a 2 step process.

1. Run the cache using the Helm chart

## 1. Run the provider using the Helm chart

#### Helm Command

```bash
helm install myprovidercache \
    oci://us-central1-docker.pkg.dev/lavanet-public/charts/lava-cache \
    --values myvalues.yaml
```

#### Parameters Description

- **`chain-id`** - The ID of the serviced chain (e.g., **`COS4`** or **`FTM250`**).
- **`amount`** - Stake amount for the specific chain (e.g., **`2010ulava`**).
- **`endpoint`** - Provider host listener, composed of `provider-host:provider-port,geolocation`.
- **`geolocation`** - Indicates the geographical location where the process is located (e.g., **`1`** for US or **`2`** for EU).

#### Flags Details

- **`--expiration`** __duration__ - how long does a cache entry lasts in the cache for a finalized entry (default 1h0m0s)
- **`--expiration-finalized-node-errors duration   how long does a cache entry lasts in the cache for a finalized node error entry (default 5s)
--expiration-multiplier float                 Multiplier for finalized cache entry expiration. 1 means no change (default), 1.2 means 20% longer. (default 1)
--expiration-non-finalized duration           how long does a cache entry lasts in the cache for a non finalized entry (default 500ms)
--expiration-non-finalized-multiplier float   Multiplier for non-finalized cache entry expiration. 1 means no change (default), 1.2 means 20% longer. (default 1)
-h, --help                                        help for cache
--log_level string                            The logging level (trace|debug|info|warn|error|fatal|panic) (default "info")
--max-items int                               the maximal amount of entries to save (default 2147483648)
--metrics_address string                      address to listen to prometheus metrics 127.0.0.1:5555, later you can curl http://127.0.0.1:5555/metrics (default "disabled")

- **`--from`** - The account to be used for the provider staking (e.g., **`my_account`**).
- **`--gas`** - The gas limit for the transaction (e.g., **`"auto"`**).
- **`--gas-adjustment`** - The gas adjustment factor (e.g., **`"1.5"`**).
- **`--node`** - A RPC node for Lava (e.g., **`https://public-rpc-testnet2.lavanet.xyz:443/rpc/`**).

For full docs on [how to stake as a provider](https://docs.lavanet.xyz/provider-setup#step-2-stake-as-provider) please see our docs: https://docs.lavanet.xyz/provider-setup#step-2-stake-as-provider

## Resources

- Provider setup docs: https://docs.lavanet.xyz/provider-setup#step-2-stake-as-provider
